from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, Skill, Message
from forms import LoginForm, RegistrationForm, EditProfileForm
from extensions import db, login_manager

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
@login_required
def profile():
    skills_known = current_user.skills.filter_by(category='known').all()
    skills_learning = current_user.skills.filter_by(category='learning').all()
    return render_template('profile.html',
                         user=current_user,
                         skills_known=skills_known,
                         skills_learning=skills_learning)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        
        # Update skills
        current_user.skills.filter_by(category='known').delete()
        current_user.skills.filter_by(category='learning').delete()
        
        for skill_name in form.skills_offer.data.split(','):
            if skill_name.strip():
                skill = Skill(name=skill_name.strip(), category='known', user_id=current_user.id)
                db.session.add(skill)
        
        for skill_name in form.skills_learn.data.split(','):
            if skill_name.strip():
                skill = Skill(name=skill_name.strip(), category='learning', user_id=current_user.id)
                db.session.add(skill)
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('edit-profile.html', form=form)

@main.route('/explore', methods=['GET'])
@login_required
def explore():
    search_query = request.args.get('search')
    if search_query:
        skills = Skill.query.filter(Skill.name.ilike(f'%{search_query}%')).all()
    else:
        skills = Skill.query.all()
    return render_template('explore.html', skills=skills)

@main.route('/messages')
@login_required
def messages():
    conversations = Message.query.filter(
        (Message.sender_id == current_user.id) | 
        (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    return render_template('message.html', conversations=conversations)
