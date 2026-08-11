from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    phone = db.Column(db.String(15), nullable=True)         # Made optional
    role = db.Column(db.String(50), nullable=True)          # Made optional
    
    full_name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class BugReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    steps_to_reproduce = db.Column(db.Text)
    environment = db.Column(db.String(255))
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign Key to User (assignee)
    attachments = db.Column(db.ARRAY(db.String))  # Store file paths or URLs as an array
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with User to get the assignee details
    assignee_user = db.relationship('User', backref=db.backref('assigned_bugs', lazy=True))
