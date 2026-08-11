from flask_mail import Message
from extensions import mail

def send_verification_code(email, code):
    msg = Message('BugTracker Password Reset Code', recipients=[email])
    msg.body = f'Your verification code is: {code}'

    try:
        mail.send(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
