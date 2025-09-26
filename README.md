# Flask Items Manager - Multi-User Edition

A beautiful, professional item management application with complete user authentication system.

## Live Demo

Visit the live application: https://item-manager-0en1.onrender.com

## Features

### Authentication System
- Secure User Registration with email validation
- Login/Logout with Flask-Login session management  
- Password Security with Werkzeug hashing
- Remember Me functionality
- User Isolation - each user has private items

### Item Management
- Add Items with name and description
- Real-time Search to filter items instantly
- Edit & Update items with modal interface
- Delete Items with confirmation prompts
- Persistent Storage (SQLite locally, PostgreSQL in production)

### Beautiful Design
- Modern UI with purple gradient design
- Smooth animations and hover effects
- Responsive layout for all devices
- Professional typography with Segoe UI
- Interactive elements with transitions

## Tech Stack

- Flask 2.3.3 - Web Framework
- Flask-Login 0.6.2 - User Session Management
- Flask-SQLAlchemy 3.0.5 - Database ORM
- Flask-WTF 1.1.1 - Form Handling & CSRF Protection
- WTForms 3.0.1 - Form Validation
- Werkzeug 2.3.7 - Password Hashing
- HTML5/CSS3/JavaScript - Frontend

## Installation

1. Clone the repository:
   git clone https://github.com/PrathamTiwari-max/flask-app.git
   cd flask-app

2. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python app.py

5. Visit: (https://item-manager-0en1.onrender.com)

## Usage

1. Register - Create your account with username, email, and password
2. Login - Access your personal dashboard  
3. Add Items - Start building your item collection
4. Manage - Edit, delete, or search through your items
5. Logout - Secure session termination

## Security Features

- Password Hashing with Werkzeug
- CSRF Protection with Flask-WTF
- Input Sanitization for XSS prevention
- Session Security with Flask-Login
- User Isolation at database level
- SQL Injection Prevention with SQLAlchemy ORM

## Deployment

Deployed on Render with:
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Live URL: https://item-manager-0en1.onrender.com

## Developer

Pratham Tiwari
- Computer Science graduate 
- Full-Stack Developer specializing in Flask & React, python development, generative AI
- Location: Pimpri-Chinchwad, Maharashtra, India

GitHub: https://github.com/PrathamTiwari-max

## Future Enhancements

- Categories & Tags for organizing items
- Image Upload functionality
- Export to CSV/PDF
- Dark Mode toggle
- REST API endpoints
- Email verification
- Password reset functionality

Built with love by Pratham Tiwari
