from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, Skill, Message, ConnectionRequest
from forms import LoginForm, RegistrationForm, EditProfileForm
from extensions import db, login_manager
from werkzeug.utils import secure_filename
import os
import time
from sqlalchemy import func

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)

@main.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            name=form.username.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('sign-up.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    recommended_skills = Skill.query.filter_by(category='recommended').limit(3).all()
    return render_template('dashboard.html', 
                         user=current_user,
                         recommended_skills=recommended_skills)

@main.route('/profile')
@main.route('/profile/<username>')
@login_required
def profile(username=None):
    if username:
        user = User.query.filter_by(username=username).first_or_404()
    else:
        user = current_user
        
    skills_known = user.skills.filter_by(category='known').all()
    skills_learning = user.skills.filter_by(category='learning').all()
    return render_template('profile.html',
                         user=user,
                         skills_known=skills_known,
                         skills_learning=skills_learning)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    
    # Pre-populate skills fields
    if request.method == 'GET':
        skills_known = current_user.skills.filter_by(category='known').all()
        skills_learning = current_user.skills.filter_by(category='learning').all()
        
        form.skills_offer.data = ','.join([skill.name for skill in skills_known])
        form.skills_learn.data = ','.join([skill.name for skill in skills_learning])
    
    if form.validate_on_submit():
        # Update user profile data (excluding skills)
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        
        # Handle profile picture upload
        if 'profile_pic' in request.files and request.files['profile_pic'].filename:
            file = request.files['profile_pic']
            filename = secure_filename(file.filename)
            if filename:
                file_ext = os.path.splitext(filename)[1]
                if file_ext.lower() in ['.jpg', '.jpeg', '.png']:
                    new_filename = f"user_{current_user.id}_{int(time.time())}{file_ext}"
                    file.save(os.path.join('static/uploads', new_filename))
                    current_user.profile_pic = new_filename
        
        # Update skills - first remove existing skills
        current_user.skills.filter_by(category='known').delete()
        current_user.skills.filter_by(category='learning').delete()
        
        # Add skills I can offer
        if form.skills_offer.data:
            for skill_name in form.skills_offer.data.split(','):
                if skill_name.strip():
                    skill = Skill(name=skill_name.strip(), category='known', user_id=current_user.id)
                    db.session.add(skill)
        
        # Add skills I want to learn
        if form.skills_learn.data:
            for skill_name in form.skills_learn.data.split(','):
                if skill_name.strip():
                    skill = Skill(name=skill_name.strip(), category='learning', user_id=current_user.id)
                    db.session.add(skill)
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('edit-profile.html', form=form, current_user=current_user)

@main.route('/explore', methods=['GET'])
@login_required
def explore():
    search_query = request.args.get('search')
    search_type = request.args.get('search_type', 'all')
    skill_matches = []
    has_search = False
    skills = []
    
    if search_query:
        has_search = True
        # Search based on selected type
        if search_type == 'username':
            # Search for users by username
            users = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
            skills = []
            # Display a message about searching by username
        elif search_type == 'skills':
            # Search for skills users know
            skills = Skill.query.filter(
                Skill.name.ilike(f'%{search_query}%'),
                Skill.category == 'known'
            ).all()
        elif search_type == 'learning':
            # Search for skills users want to learn
            skills = Skill.query.filter(
                Skill.name.ilike(f'%{search_query}%'),
                Skill.category == 'learning'
            ).all()
        else:  # 'all' or default
            # Search for all matching skills
            skills = Skill.query.filter(Skill.name.ilike(f'%{search_query}%')).all()
    else:
        # Find matching users - current user's learning skills match others' known skills
        user_known_skills = current_user.get_known_skills()
        user_learning_skills = current_user.get_learning_skills()
        
        # Find users who know what the current user wants to learn
        potential_mentors = []
        for learning_skill in user_learning_skills:
            mentors = db.session.query(User, Skill).join(Skill, User.id == Skill.user_id)\
                .filter(User.id != current_user.id)\
                .filter(Skill.category == 'known')\
                .filter(func.lower(Skill.name) == learning_skill.lower())\
                .all()
            
            for mentor, skill in mentors:
                if not current_user.has_connection_with(mentor.id):
                    # Find what the mentor wants to learn that the current user knows
                    for mentor_learning_skill in mentor.get_learning_skills():
                        if mentor_learning_skill.lower() in [s.lower() for s in user_known_skills]:
                            # This is a match! The current user knows something the mentor wants to learn
                            # and the mentor knows something the current user wants to learn
                            mentor_skill_obj = Skill.query.filter_by(
                                user_id=mentor.id, 
                                name=skill.name, 
                                category='known'
                            ).first()
                            
                            user_skill_obj = Skill.query.filter_by(
                                user_id=current_user.id, 
                                category='known'
                            ).filter(func.lower(Skill.name) == mentor_learning_skill.lower()).first()
                            
                            if mentor_skill_obj and user_skill_obj:
                                match_data = {
                                    'user': mentor,
                                    'they_know': skill.name,
                                    'they_want_to_learn': mentor_learning_skill,
                                    'matched_skill': mentor_skill_obj,
                                    'requested_skill': user_skill_obj
                                }
                                skill_matches.append(match_data)
    
    return render_template('explore.html', 
                          has_search=has_search,
                          search_query=search_query,
                          skills=skills,
                          skill_matches=skill_matches,
                          user=current_user)

@main.route('/messages')
@login_required
def messages():
    conversations = Message.query.filter(
        (Message.sender_id == current_user.id) | 
        (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    return render_template('message.html', conversations=conversations)

@main.route('/connections', methods=['GET'])
@login_required
def connections():
    sent_requests = ConnectionRequest.query.filter_by(sender_id=current_user.id).all()
    received_requests = ConnectionRequest.query.filter_by(receiver_id=current_user.id).all()
    return render_template('connections.html', 
                           sent_requests=sent_requests, 
                           received_requests=received_requests)

@main.route('/request-connection', methods=['POST'])
@login_required
def request_connection():
    user_id = request.form.get('user_id')
    matched_skill_id = request.form.get('matched_skill_id')
    requested_skill_id = request.form.get('requested_skill_id')
    
    # Validate input
    if not user_id or not matched_skill_id or not requested_skill_id:
        flash('Invalid request parameters.', 'error')
        return redirect(url_for('main.explore'))
    
    # Check if users exist
    receiver = User.query.get(user_id)
    if not receiver:
        flash('User not found.', 'error')
        return redirect(url_for('main.explore'))
    
    # Check for existing connection request
    if current_user.has_connection_with(user_id):
        flash('A connection request already exists with this user.', 'warning')
        return redirect(url_for('main.explore'))
    
    # Create connection request
    connection = ConnectionRequest(
        sender_id=current_user.id,
        receiver_id=user_id,
        matched_skill_id=matched_skill_id,
        requested_skill_id=requested_skill_id,
        status='pending'
    )
    
    db.session.add(connection)
    db.session.commit()
    
    flash('Connection request sent successfully!', 'success')
    return redirect(url_for('main.explore'))

@main.route('/accept-connection/<int:request_id>', methods=['POST'])
@login_required
def accept_connection(request_id):
    connection = ConnectionRequest.query.get_or_404(request_id)
    
    # Verify that current user is the receiver
    if connection.receiver_id != current_user.id:
        flash('You are not authorized to accept this request.', 'error')
        return redirect(url_for('main.connections'))
    
    # Update status
    connection.status = 'accepted'
    db.session.commit()
    
    # Create initial message to start the conversation
    message = Message(
        content=f"Hello! I accepted your connection request for skill swapping. Let's chat about how we can help each other learn!",
        sender_id=current_user.id,
        receiver_id=connection.sender_id,
        is_read=False
    )
    
    db.session.add(message)
    db.session.commit()
    
    flash('Connection accepted! A message thread has been created.', 'success')
    return redirect(url_for('main.messages'))

@main.route('/reject-connection/<int:request_id>', methods=['POST'])
@login_required
def reject_connection(request_id):
    connection = ConnectionRequest.query.get_or_404(request_id)
    
    # Verify that current user is the receiver
    if connection.receiver_id != current_user.id:
        flash('You are not authorized to reject this request.', 'error')
        return redirect(url_for('main.connections'))
    
    # Update status
    connection.status = 'rejected'
    db.session.commit()
    
    flash('Connection request rejected.', 'success')
    return redirect(url_for('main.connections'))
