from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import db
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.forms.auth_form import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            role=UserRole[form.role.data],
            department=form.department.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Log the registration Audit
        AuditLog.create_log('User Registration', request, user_id=user.id, resource_type='User', resource_id=user.id)
        
        # Log the user in directly after registration
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if input is email or username
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data)).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember.data)
        
        # Log the login Audit
        AuditLog.create_log('User Login', request, user_id=user.id, resource_type='User', resource_id=user.id)
        
        # If user was redirected here from a protected page, redirect them back
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
            
        flash(f'Logged in successfully as {user.role.name}.', 'success')
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    
    # Log the logout Audit
    AuditLog.create_log('User Logout', request, user_id=user_id)
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
