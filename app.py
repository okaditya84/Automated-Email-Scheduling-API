# app.py
from flask import Flask, request, jsonify
from celery import Celery
from datetime import datetime, timedelta
from models import db, ScheduledEmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

celery = Celery(app.name, broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
celery.conf.update(app.config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/schedule-email', methods=['POST'])
def schedule_email():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        required_fields = ['recipient', 'subject', 'body', 'schedule_time']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        recipient = data['recipient']
        subject = data['subject']
        body = data['body']
        schedule_time = datetime.fromisoformat(data['schedule_time'])
        recurrence = data.get('recurrence')
        attachments = json.dumps(data.get('attachments', []))  # Convert to JSON string

        email = ScheduledEmail(recipient=recipient, subject=subject, body=body, 
                               schedule_time=schedule_time, recurrence=recurrence,
                               attachments=attachments)
        db.session.add(email)
        db.session.commit()

        schedule_task.apply_async(args=[email.id], eta=schedule_time)

        return jsonify({"message": "Email scheduled successfully", "id": email.id}), 201
    except Exception as e:
        logger.error(f"Error in schedule_email: {str(e)}")
        return jsonify({"error": "An error occurred while scheduling the email"}), 500

@app.route('/scheduled-emails', methods=['GET'])
def get_scheduled_emails():
    try:
        emails = ScheduledEmail.query.all()
        return jsonify([email.to_dict() for email in emails])
    except Exception as e:
        logger.error(f"Error in get_scheduled_emails: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving scheduled emails"}), 500

@app.route('/scheduled-emails/<int:id>', methods=['GET'])
def get_scheduled_email(id):
    try:
        email = ScheduledEmail.query.get_or_404(id)
        return jsonify(email.to_dict())
    except Exception as e:
        logger.error(f"Error in get_scheduled_email: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the email"}), 500

@app.route('/scheduled-emails/<int:id>', methods=['DELETE'])
def cancel_scheduled_email(id):
    try:
        email = ScheduledEmail.query.get_or_404(id)
        db.session.delete(email)
        db.session.commit()
        return jsonify({"message": "Email scheduling cancelled"}), 200
    except Exception as e:
        logger.error(f"Error in cancel_scheduled_email: {str(e)}")
        return jsonify({"error": "An error occurred while cancelling the email"}), 500

@celery.task
def schedule_task(email_id):
    with app.app_context():
        try:
            email = ScheduledEmail.query.get(email_id)
            if email:
                send_email(email)
                if email.recurrence:
                    next_schedule = calculate_next_schedule(email)
                    email.schedule_time = next_schedule
                    db.session.commit()
                    schedule_task.apply_async(args=[email.id], eta=next_schedule)
                else:
                    db.session.delete(email)
                    db.session.commit()
        except Exception as e:
            logger.error(f"Error in schedule_task: {str(e)}")

def send_email(email):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_USERNAME')
        msg['To'] = email.recipient
        msg['Subject'] = email.subject
        msg.attach(MIMEText(email.body, 'plain'))

        # Here you would add logic to handle attachments
        # You can parse the JSON string back into a list
        attachments = json.loads(email.attachments)
        # Add your attachment handling logic here

        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
        logger.info(f"Email sent successfully to {email.recipient}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")

def calculate_next_schedule(email):
    if email.recurrence == 'daily':
        return email.schedule_time + timedelta(days=1)
    elif email.recurrence == 'weekly':
        return email.schedule_time + timedelta(weeks=1)
    elif email.recurrence == 'monthly':
        next_month = email.schedule_time.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=min(email.schedule_time.day, next_month.day))
    elif email.recurrence == 'quarterly':
        next_quarter = email.schedule_time + timedelta(days=91)
        return next_quarter.replace(day=min(email.schedule_time.day, next_quarter.day))

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)