import os

class Config:
    # Secret key for sessions, CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # PostgreSQL Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:siddhesh@localhost/bug_tracking_system'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # to suppress warning

    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bug75297@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'kedr lbin nufg fcqb')  # App password (not Gmail password)
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
