# SkillSwap Codebase Documentation

This document provides a detailed explanation of each component and functionality in the SkillSwap application codebase. The application is built using Flask, a Python web framework, and follows a modular architecture for maintainability and scalability.

## Problem Statement & Solution

### The Problem

In today's rapidly evolving world, individuals face several challenges related to skill development and knowledge exchange:

1. **Skill Gap**: There is a growing disconnect between the skills people have and the skills needed in the modern workforce.
2. **Expensive Education**: Traditional education and skill development resources are often expensive and inaccessible to many.
3. **Untapped Knowledge**: People possess valuable skills and knowledge that remain unutilized because they lack platforms to share them.
4. **Isolated Learning**: Learning often happens in isolation, without community support or practical application.
5. **Limited Networking**: People with complementary skills rarely connect in meaningful ways that could lead to skill exchange.

### Our Solution

SkillSwap addresses these challenges by creating a community-driven platform where users can exchange skills directly with one another:

1. **Peer-to-Peer Learning**: Users can teach what they know and learn what they want to know directly from others.
2. **Skill Marketplace**: The platform matches people based on complementary skill sets, creating a barter economy for knowledge.
3. **Community Building**: Users form connections based on shared learning interests and teaching capabilities.
4. **Accessible Education**: By removing financial barriers and enabling direct exchange, learning becomes more accessible.
5. **Practical Application**: Skills are taught by practitioners with real-world experience rather than through theoretical frameworks alone.

### Logo & Brand Significance

The SkillSwap logo and brand identity represent the core values and vision of the platform:

1. **Interlocking Puzzle Pieces**: The logo features two interlocking puzzle pieces in blue and green, symbolizing:
   - The perfect fit between those who want to teach and those who want to learn
   - The complementary nature of skill exchange
   - The idea that everyone has something to contribute to the whole

2. **Color Palette**:
   - **Blue** (Primary color, #3b82f6): Represents trust, knowledge, and reliability
   - **Green** (Accent color, #10b981): Symbolizes growth, learning, and the value exchange
   - The gradient between them illustrates the seamless flow of knowledge between individuals

3. **Typography**: The clean, modern font reflects the platform's focus on accessibility and clarity, while the slight rounded edges convey the friendly, community-oriented nature of the service.

4. **Tagline**: "Learn. Teach. Grow Together." encapsulates the platform's mission of reciprocal learning and community development.

Through its design and functionality, SkillSwap embodies the idea that everyone is both a teacher and a student, and that through mutual exchange, communities can solve their own skill gaps collaboratively.

## Table of Contents

1. [Problem Statement & Solution](#problem-statement--solution)
2. [Application Structure](#application-structure)
3. [Core Components](#core-components)
4. [Database Models](#database-models)
5. [Routes and Views](#routes-and-views)
6. [Forms](#forms)
7. [Templates](#templates)
8. [Static Files](#static-files)
9. [Utility Functions](#utility-functions)
10. [Configuration](#configuration)
11. [Authentication System](#authentication-system)
12. [Database Initialization](#database-initialization)

## Application Structure

The SkillSwap application follows a modular structure with separation of concerns:

```
skillswap/
│
├── app.py                # Application factory and entry point
├── config.py             # Configuration settings
├── extensions.py         # Flask extensions initialization
├── models.py             # Database models
├── routes.py             # Route definitions and view functions
├── forms.py              # Form classes for data validation
├── filters.py            # Custom template filters
├── init_db.py            # Database initialization script
│
├── static/               # Static assets (CSS, JavaScript, images)
│   ├── css/              # CSS stylesheets
│   ├── js/               # JavaScript files
│   └── assets/           # Images and other assets
│
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with common structure
│   ├── index.html        # Homepage template
│   ├── login.html        # Login page
│   └── ...               # Other page templates
│
├── instance/             # Instance-specific data (database, secrets)
│   └── skillswap.db      # SQLite database file
│
└── requirements.txt      # Python dependencies
```

## Core Components

### app.py

The `app.py` file serves as the entry point to the application and contains the application factory function. It includes:

- `create_app()` function that initializes and configures the Flask application
- Extension initialization and configuration
- Blueprint registration
- Custom template filter registration
- Error handler registration
- Application instance creation

```python
# Key functionality:
# - Flask application initialization and configuration
# - Extension initialization (SQLAlchemy, Flask-Login, Flask-Migrate)
# - Blueprint registration for modular routes
# - Custom filter registration
# - Error handler setup (404 and 500 pages)
```

### extensions.py

The `extensions.py` file initializes Flask extensions used throughout the application:

- `SQLAlchemy` - ORM for database operations
- `LoginManager` - Handles user authentication
- `Migrate` - Database migration utility

The login manager settings are configured to:
- Direct unauthenticated users to the login page (`main.login`)
- Use the "info" category for flash messages

## Database Models

### models.py

The `models.py` file defines the database schema using SQLAlchemy ORM. It contains three main models:

#### User Model
Represents application users with the following attributes:
- `id`: Unique identifier (primary key)
- `username`: Unique username (80 characters max)
- `email`: Unique email address (120 characters max)
- `password_hash`: Securely hashed password (128 characters)
- `name`: User's full name (100 characters max)
- `location`: User's location (100 characters max)
- `bio`: User's biography (text field)
- `profile_pic`: Path to profile picture (200 characters max)
- `created_at`: Account creation timestamp
- `last_seen`: Last activity timestamp

Relationships:
- `skills`: One-to-many relationship with Skill model
- `sent_messages`: One-to-many relationship with Message model (sender)
- `received_messages`: One-to-many relationship with Message model (receiver)

Methods:
- `set_password()`: Hashes and stores password
- `check_password()`: Verifies password against stored hash

#### Skill Model
Represents skills that users know or want to learn:
- `id`: Unique identifier (primary key)
- `name`: Skill name (100 characters max)
- `category`: Classification (known, learning, recommended)
- `user_id`: Foreign key linking to User model
- `created_at`: Skill creation timestamp

#### Message Model
Represents messages between users:
- `id`: Unique identifier (primary key)
- `content`: Message content (text field)
- `sender_id`: Foreign key linking to sender (User model)
- `receiver_id`: Foreign key linking to receiver (User model)
- `is_read`: Boolean flag for read status
- `created_at`: Message creation timestamp

## Routes and Views

### routes.py

The `routes.py` file defines all application routes and view functions using a Flask Blueprint:

#### Authentication Routes

- `@main.route('/')`: Index route, renders the homepage
  - Method: GET
  - No authentication required
  - Renders: `index.html`

- `@main.route('/login')`: User login
  - Methods: GET, POST
  - Form processing for user authentication
  - Redirects authenticated users to dashboard
  - Renders: `login.html`

- `@main.route('/sign-up')`: User registration
  - Methods: GET, POST
  - Form processing for new user registration
  - Redirects to login after successful registration
  - Renders: `sign-up.html`

- `@main.route('/logout')`: User logout
  - Method: GET
  - Authentication required
  - Logs out current user and redirects to homepage

#### User Routes

- `@main.route('/dashboard')`: User dashboard
  - Method: GET
  - Authentication required
  - Displays recommended skills
  - Renders: `dashboard.html`

- `@main.route('/profile')`: User profile
  - Method: GET
  - Authentication required
  - Shows user's known and learning skills
  - Renders: `profile.html`

- `@main.route('/edit-profile')`: Edit user profile
  - Methods: GET, POST
  - Authentication required
  - Form processing for profile updates
  - Handles skill addition and removal
  - Renders: `edit-profile.html`

#### Feature Routes

- `@main.route('/explore')`: Explore skills
  - Method: GET
  - Authentication required
  - Search functionality for skills
  - Renders: `explore.html`

- `@main.route('/messages')`: User messages
  - Method: GET
  - Authentication required
  - Displays user conversations
  - Renders: `message.html`

## Forms

### forms.py

The `forms.py` file defines form classes using Flask-WTF for validation and processing:

#### LoginForm
User login form with:
- Username field with required validation
- Password field with required validation
- Submit button

#### RegistrationForm
User registration form with:
- Username field (4-25 characters, required)
- Email field with email validation
- Password field with required validation
- Password confirmation field with equality validation
- Submit button

Custom validations:
- `validate_username()`: Ensures username is unique
- `validate_email()`: Ensures email is unique

#### EditProfileForm
Profile editing form with:
- Name field (up to 100 characters)
- Location field (up to 100 characters)
- Biography field (up to 500 characters)
- Skills to offer field (comma-separated)
- Skills to learn field (comma-separated)
- Submit button

## Templates

The application uses Jinja2 templates located in the `templates/` directory:

### Base Templates
- `base.html`: Main layout template with common elements
- `404.html`: Not found error page
- `500.html`: Server error page

### Page Templates
- `index.html`: Homepage/landing page
- `login.html`: User login page
- `sign-up.html`: User registration page
- `dashboard.html`: User dashboard with recommended skills
- `profile.html`: User profile page showing their skills
- `edit-profile.html`: Profile editing page
- `explore.html`: Skill exploration and search page
- `message.html`: Messaging interface
- `sidebar.html`: Sidebar navigation component

## Static Files

The application uses structured static files in the `static/` directory:

### CSS Files
Organized in `static/css/`:
- `general.css`: Global styles and variables
- `navbar.css`: Navigation bar styles
- `sidebar.css`: Sidebar navigation styles
- `dashboard.css`: Dashboard page styles
- `profile.css`: Profile page styles
- `edit-profile.css`: Profile editing page styles
- `explore.css`: Exploration page styles
- `login.css`: Login page styles
- `sign-up.css`: Registration page styles
- `message.css`: Messaging interface styles

### JavaScript Files
Located in `static/js/`:
- Client-side functionality and interactions

### Assets
Located in `static/assets/`:
- Images, icons, and other media files

## Utility Functions

### filters.py

The `filters.py` file defines custom template filters for enhanced display:

#### time_ago
A custom Jinja2 filter that:
- Takes a timestamp as input
- Returns a human-readable relative time string (e.g., "2 hours ago")
- Handles different time intervals (seconds, minutes, hours, days)
- Properly pluralizes time units

## Configuration

### config.py

The `config.py` file contains application configuration settings using a class-based approach:

#### Config Class
Defines application configuration with:
- `SECRET_KEY`: Secure key for CSRF protection (from environment variable or default)
- `SQLALCHEMY_DATABASE_URI`: Database connection string (SQLite by default)
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disables modification tracking for performance
- `ALLOWED_EXTENSIONS`: Permitted file types for uploads
- `UPLOAD_FOLDER`: Path for file uploads

Uses python-dotenv to load environment variables from a `.env` file.

## Authentication System

The authentication system is built with Flask-Login and includes:

- User authentication with username/password
- Secure password hashing with Werkzeug
- Login required protection for routes
- User session management
- Redirect to login page for unauthorized access

## Database Initialization

### init_db.py

The `init_db.py` script initializes the database:
- Creates a Flask application context
- Creates all database tables defined in models
- Provides confirmation message upon completion

This script needs to be run when setting up the application for the first time or after structural changes to the database models.

---

## Summary of Key Features

1. **User Authentication**: Registration, login, and session management
2. **User Profiles**: Personal information and skill management
3. **Skill Management**: Users can list skills they know and want to learn
4. **Skill Exploration**: Search and discover skills from other users
5. **Messaging System**: Communication between users
6. **Responsive Design**: Modern UI with consistent styling
7. **Flash Messages**: User feedback for actions
8. **Form Validation**: Client and server-side validation
9. **Database ORM**: Structured data management with SQLAlchemy
10. **Modular Architecture**: Separation of concerns for maintainability

---

*Created on April 1st, 2025* 