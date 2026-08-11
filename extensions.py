from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

# Database extension
db = SQLAlchemy()

# CSRF protection for forms
csrf = CSRFProtect()

# Flask-Mail for sending emails
mail = Mail()
