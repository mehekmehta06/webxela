from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the email server from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('EMAIL_PASSWORD')

contact = Flask(__name__)

def send_thank_you_email(recipient_email, recipient_name):
    subject = "Thank You for Your Submission"
    body = f"Dear {recipient_name},\n\nThank you for reaching out to us. We have received your message and will get back to you shortly.\n\nBest regards,\nYour Company"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = recipient_email
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

@contact.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    company_name = data.get('company_name')
    phone_no = data.get('phone_no')
    message = data.get('message')
    
    if not all([name, email,company_name,phone_no, message]):
        return jsonify({"error": "Missing data"}), 400
    
    # Send the thank you email
    send_thank_you_email(email, name)
    
    return jsonify({"message": "Form submitted successfully"}), 200

if __name__ == '__main__':
    contact.run(debug=True)
