from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Item
from forms import RegistrationForm, LoginForm
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-development-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for now

# Initialize extensions
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful! Welcome back!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

# Main Application Routes
@app.route('/')
@login_required
def index():
    items = Item.query.filter_by(user_id=current_user.id).order_by(Item.created_at.desc()).all()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if name:
        try:
            item = Item(
                name=name,
                description=description if description else None,
                user_id=current_user.id
            )
            db.session.add(item)
            db.session.commit()
            flash(f'Item "{name}" added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding item. Please try again.', 'danger')
    else:
        flash('Item name is required!', 'danger')
    
    return redirect(url_for('index'))

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        item_name = item.name
        db.session.delete(item)
        db.session.commit()
        flash(f'Item "{item_name}" deleted successfully!', 'success')
    else:
        flash('Item not found!', 'danger')
    
    return redirect(url_for('index'))

@app.route('/update_item/<int:item_id>', methods=['POST'])
@login_required
def update_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        new_name = request.form.get('name', '').strip()
        new_description = request.form.get('description', '').strip()
        
        if new_name:
            item.name = new_name
            item.description = new_description if new_description else None
            db.session.commit()
            flash(f'Item "{new_name}" updated successfully!', 'success')
        else:
            flash('Item name cannot be empty!', 'danger')
    else:
        flash('Item not found!', 'danger')
    
    return redirect(url_for('index'))

# Database initialization
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
