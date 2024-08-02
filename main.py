from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import EmailScheduleCreate, EmailSchedule
from models import EmailSchedule as EmailScheduleModel
import crud
from celery import Celery
from celery_config import celery_app
from tasks import send_scheduled_email
from datetime import datetime, timedelta
from datetime import datetime
import pytz

app = FastAPI()

Base.metadata.create_all(bind=engine)

# @app.post("/schedule-email/", response_model=EmailSchedule)
# def schedule_email(email_schedule: EmailScheduleCreate, db: Session = Depends(get_db)):
#     db_email_schedule = crud.create_email_schedule(db, email_schedule)
#     delay = (email_schedule.schedule_time - datetime.utcnow()).total_seconds()
#     celery_app.send_task("tasks.send_scheduled_email", args=[db_email_schedule.id], countdown=delay)
#     return db_email_schedule

@app.post("/schedule-email/")
def schedule_email(email_schedule: EmailSchedule):
    # Assign a unique id to the email schedule
    email_schedule.id = len(scheduled_emails) + 1

    schedule_time = email_schedule.schedule_time.astimezone(pytz.UTC)
    current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
    delay = (schedule_time - current_time).total_seconds()

    task_id = None
    if delay > 0:
        if email_schedule.recurring:
            task_id = schedule_recurring_email.apply_async((email_schedule.dict(),), eta=schedule_time)
        else:
            task_id = send_email.apply_async((email_schedule.dict(),), countdown=delay)

    if task_id:
        scheduled_emails[email_schedule.id] = email_schedule.dict()
        scheduled_emails[email_schedule.id]["task_id"] = task_id.id

    return email_schedule.dict()

@app.get("/scheduled-emails/", response_model=list[EmailSchedule])
def read_email_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    email_schedules = crud.get_email_schedules(db, skip=skip, limit=limit)
    return email_schedules

@app.get("/scheduled-emails/{id}", response_model=EmailSchedule)
def read_email_schedule(id: int, db: Session = Depends(get_db)):
    db_email_schedule = crud.get_email_schedule(db, id)
    if db_email_schedule is None:
        raise HTTPException(status_code=404, detail="Email schedule not found")
    return db_email_schedule

@app.delete("/scheduled-emails/{id}", response_model=EmailSchedule)
def delete_email_schedule(id: int, db: Session = Depends(get_db)):
    success = crud.delete_email_schedule(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Email schedule not found")
    return {"detail": "Email schedule deleted successfully"}

