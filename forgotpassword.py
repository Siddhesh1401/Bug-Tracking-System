from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash
import random, string
from models import db, User
from send_email import send_verification_code

forgot_password_bp = Blueprint('forgot_password', __name__)

# In-memory store for verification codes (use Redis/DB for production)
verification_codes = {}

# Utility function to generate a 6-digit code
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Step 1: Request verification code
@forgot_password_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()
    if user:
        code = generate_verification_code()
        verification_codes[email] = code
        send_verification_code(email, code)
        session['reset_email'] = email
        return jsonify({"message": "Verification code sent successfully!"}), 200
    return jsonify({"message": "Email not found!"}), 404

# Step 2: Verify the code
@forgot_password_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    code = data.get("verification_code")
    email = session.get('reset_email')

    if not email:
        return jsonify({"message": "Session expired. Please try again."}), 400

    if verification_codes.get(email) == code:
        return jsonify({"message": "Code verified successfully!"}), 200
    return jsonify({"message": "Invalid verification code!"}), 400

# Step 3: Reset the password
@forgot_password_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = session.get('reset_email')

    if not email:
        return jsonify({"message": "Session expired. Try again."}), 400

    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not new_password or not confirm_password:
        return jsonify({"message": "Please fill out both password fields."}), 400

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match!"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        session.pop('reset_email', None)
        verification_codes.pop(email, None)  # Optional: clean up
        return jsonify({"message": "Password reset successful!"}), 200

    return jsonify({"message": "User not found!"}), 404
@forgot_password_bp.route('/forgot-password', methods=['GET'])
def forgot_password_page():
    return render_template('forgot_password.html')
