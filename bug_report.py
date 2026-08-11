from flask import Blueprint, request, render_template, redirect, flash, url_for
from models import BugReport
from extensions import db
import os

# Define the bug report blueprint
bug_report_bp = Blueprint('bug_report', __name__, url_prefix='/bug_report')

@bug_report_bp.route('/new', methods=['GET', 'POST'])
def new_bug_report():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        bug_type = request.form['type']
        priority = request.form['priority']
        steps = request.form['steps']
        expected = request.form['expected']
        actual = request.form['actual']
        
        # Handle file uploads
        files = request.files.getlist('screenshot')  # List of files
        file_paths = []
        if files:
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            for file in files:
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)
                file_paths.append(file_path)

        # Create a new BugReport entry
        bug_report = BugReport(
            title=title,
            description=description,
            type=bug_type,
            priority=priority,
            steps_to_reproduce=steps,
            expected_behavior=expected,
            actual_behavior=actual,
            attachments=file_paths
        )

        # Save to the database
        db.session.add(bug_report)
        db.session.commit()

        flash('Bug report submitted successfully!', 'success')
        return redirect(url_for('bug_report.new_bug_report'))

    return render_template('mnewbugreport.html')  # Render the bug report form
