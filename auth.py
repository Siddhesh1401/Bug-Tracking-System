from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, BugReport, db
from functools import wraps
import logging
import os
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)
logging.basicConfig(level=logging.INFO)

# ---------------- DECORATORS ----------------
def login_required(role=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please login first.", "error")
                return redirect(url_for('auth.login'))
            if role and session.get('user_role') != role:
                flash("Access denied.", "error")
                return redirect(url_for('auth.login'))
            return view_func(*args, **kwargs)
        return wrapper
    return decorator

# ---------------- SIGNUP STEP 1 ----------------
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role')

        if not all([email, phone, password, confirm_password, role]):
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.signup'))

        session['signup_data'] = {
            'email': email,
            'phone': phone,
            'password': password,
            'role': role
        }

        return redirect(url_for('auth.signup_step2'))

    return render_template('signup1.html')

# ---------------- SIGNUP STEP 2 ----------------
@auth.route('/signup/step2', methods=['GET', 'POST'])
def signup_step2():
    signup_data = session.get('signup_data')

    if not signup_data:
        flash("Session expired. Please sign up again.", "error")
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        full_name = request.form.get('fullName')
        employee_id = request.form.get('employeeId')
        gender = request.form.get('gender')
        age = request.form.get('age')

        if not all([full_name, employee_id, gender, age]):
            flash("Please fill all fields in step 2.", "error")
            return redirect(url_for('auth.signup_step2'))

        if not age.isdigit():
            flash("Age must be a valid number.", "error")
            return redirect(url_for('auth.signup_step2'))

        try:
            user = User(
                email=signup_data['email'],
                password=generate_password_hash(signup_data['password'], method='pbkdf2:sha256', salt_length=16),
                full_name=full_name,
                employee_id=employee_id,
                gender=gender,
                age=int(age),
                phone=signup_data['phone'],
                role=signup_data['role']
            )

            db.session.add(user)
            db.session.commit()

            session.pop('signup_data', None)
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error during signup: {e}")
            flash("An error occurred. Please try again.", "error")

    return render_template('signup2.html')

# ---------------- LOGIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role.lower()
            flash("Login successful!", "success")
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Invalid email or password.", "error")

    return render_template('login.html')

# ---------------- DASHBOARD ----------------
@auth.route('/dashboard')
@login_required()
def dashboard():
    role = session.get('user_role')
    if role == 'manager':
        return redirect(url_for('auth.manager_dashboard'))
    elif role == 'developer':
        return redirect(url_for('auth.developer_dashboard'))
    else:
        logging.warning(f"Unknown role: {role}")
        flash("Unknown role.", "error")
        return redirect(url_for('auth.login'))

# ---------------- MANAGER DASHBOARD ----------------
@auth.route('/manager-dashboard')
@login_required(role='manager')
def manager_dashboard():
    user = User.query.get(session['user_id'])
    return render_template('manager_dashboard.html', user=user)

# ---------------- DEVELOPER DASHBOARD ----------------
@auth.route('/developer-dashboard')
@login_required(role='developer')
def developer_dashboard():
    user = User.query.get(session['user_id'])
    return render_template('developer_dashboard.html', user=user)

# ---------------- BUGS ISSUED (Developer Only) ----------------
@auth.route('/bugs-issued')
@login_required(role='developer')
def bugs_issued():
    user = User.query.get(session['user_id'])
    return render_template('dbugissued.html', user=user)

# ---------------- WORK STATUS (Developer Only) ----------------
@auth.route('/work-status')
@login_required(role='developer')
def work_status():
    user = User.query.get(session['user_id'])
    return render_template('dworkstatus.html', user=user)

# ---------------- PROFILE ----------------
@auth.route('/profile')
@login_required()
def profile():
    user = User.query.get(session['user_id'])
    if user.role.lower() == 'developer':
        return render_template('dprofile.html', user=user)
    return render_template('mprofile.html', user=user)

# ---------------- LOGOUT ----------------
@auth.route('/logout')
@login_required()
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.login'))

# ---------------- REPORT BUG (Manager Only) ----------------
@auth.route('/report-bug')
@login_required(role='manager')
def report_bug():
    return render_template('mreportbug.html')

# ---------------- BUG STATUS (Manager Only) ----------------
@auth.route('/bug-status')
@login_required(role='manager')
def bug_status():
    return render_template('mstatus.html')

# ---------------- NEW BUG REPORT ----------------
@auth.route('/new-bug-report', methods=['GET', 'POST'])
@login_required(role='manager')  # Ensure only managers can report bugs
def new_bug_report():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        bug_type = request.form.get('type')
        priority = request.form.get('priority')
        description = request.form.get('description')
        steps_to_reproduce = request.form.get('steps')
        environment = request.form.get('environment')
        assignee_id = request.form.get('assignee')  # Can be selected from users
        attachments = request.files.getlist('attachments')

        if not all([title, bug_type, priority, description]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('auth.new_bug_report'))

        # Save attachments if they exist
        attachment_paths = []
        for attachment in attachments:
            if attachment:
                filename = secure_filename(attachment.filename)
                upload_path = os.path.join('static/uploads', filename)
                attachment.save(upload_path)
                attachment_paths.append(upload_path)

        # Create new BugReport object
        bug_report = BugReport(
            title=title,
            type=bug_type,
            priority=priority,
            description=description,
            steps_to_reproduce=steps_to_reproduce,
            environment=environment,
            assignee=assignee_id,
            attachments=attachment_paths
        )

        # Add to database
        try:
            db.session.add(bug_report)
            db.session.commit()
            flash('Bug report submitted successfully!', 'success')
            return redirect(url_for('auth.manager_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the bug report.', 'error')

    # Render the bug report submission page
    users = User.query.filter_by(role='developer').all()  # Assuming assignee should be a developer
    return render_template('mnewbugreport.html', users=users)
