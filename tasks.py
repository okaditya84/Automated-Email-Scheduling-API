from celery import Celery
from email_utils import send_email
from models import EmailSchedule
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from celery_config import celery_app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def send_scheduled_email(email_schedule_id: int):
    db = SessionLocal()
    email_schedule = db.query(EmailSchedule).filter(EmailSchedule.id == email_schedule_id).first()
    if email_schedule:
        send_email(email_schedule.recipient, email_schedule.subject, email_schedule.body)
        email_schedule.is_sent = True
        db.commit()
    db.close()
