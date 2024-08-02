from sqlalchemy.orm import Session
from models import EmailSchedule
from schemas import EmailScheduleCreate
from sqlalchemy.orm import Session
from models import EmailSchedule

def create_email_schedule(db: Session, email_schedule: EmailScheduleCreate):
    db_email_schedule = EmailSchedule(**email_schedule.dict())
    db.add(db_email_schedule)
    db.commit()
    db.refresh(db_email_schedule)
    return db_email_schedule

def get_email_schedules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(EmailSchedule).offset(skip).limit(limit).all()

def get_email_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmailSchedule).offset(skip).limit(limit).all()

def delete_email_schedule(db: Session, email_schedule_id: int):
    db_email_schedule = db.query(EmailSchedule).filter(EmailSchedule.id == email_schedule_id).first()
    if db_email_schedule:
        db.delete(db_email_schedule)
        db.commit()
        return True
    return False
