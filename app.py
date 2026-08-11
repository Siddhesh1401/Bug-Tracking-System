from flask import Flask
from config import Config
from extensions import db, mail
from auth import auth
from forgotpassword import forgot_password_bp
from bug_report import bug_report_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(forgot_password_bp)
    app.register_blueprint(bug_report_bp)  # Register the bug_report blueprint

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
