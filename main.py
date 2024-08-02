

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
import pytz

app = FastAPI()

Base.metadata.create_all(bind=engine)



from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import EmailScheduleCreate, EmailSchedule, DeleteResponse
from models import EmailSchedule as EmailScheduleModel
import crud
from celery import Celery
from celery_config import celery_app
from tasks import send_scheduled_email
from datetime import datetime, timedelta
import pytz

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/schedule-email/", response_model=EmailSchedule)
def schedule_email(email_schedule: EmailScheduleCreate, db: Session = Depends(get_db)):
    schedule_time = email_schedule.schedule_time.replace(tzinfo=pytz.UTC)
    current_time = datetime.now(pytz.UTC)
    delay = (schedule_time - current_time).total_seconds()

    if delay > 0:
        db_email_schedule = crud.create_email_schedule(db, email_schedule)
        
        if email_schedule.recurring:
            # Handle recurring emails (you'll need to implement this)
            pass
        else:
            send_scheduled_email.apply_async((db_email_schedule.id,), countdown=delay)

        return db_email_schedule
    else:
        raise HTTPException(status_code=400, detail="Schedule time must be in the future")

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

@app.delete("/scheduled-emails/{id}", response_model=DeleteResponse)
def delete_email_schedule(id: int, db: Session = Depends(get_db)):
    success = crud.delete_email_schedule(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Email schedule not found")
    return DeleteResponse(detail="Email schedule deleted successfully")