from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base

class EmailSchedule(Base):
    __tablename__ = "email_schedules"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True)
    subject = Column(String)
    body = Column(String)
    schedule_time = Column(DateTime)
    recurring = Column(Boolean, default=False)
    recurrence_type = Column(String, nullable=True)  # daily, weekly, monthly, quarterly
    recurrence_value = Column(String, nullable=True)  # time/day/etc.
    is_sent = Column(Boolean, default=False)
