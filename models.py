from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base

class EmailSchedule(Base):
    __tablename__ = "email_schedules"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True)
    subject = Column(String)
    body = Column(String)
    schedule_time = Column(DateTime)
    recurring = Column(Boolean)
    recurrence_type = Column(String, nullable=True)
    recurrence_value = Column(String, nullable=True)
    is_sent = Column(Boolean, default=False)