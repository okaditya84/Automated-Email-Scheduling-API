from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmailScheduleCreate(BaseModel):
    recipient: str
    subject: str
    body: str
    schedule_time: datetime
    recurring: Optional[bool] = False
    recurrence_type: Optional[str] = None
    recurrence_value: Optional[str] = None

class EmailSchedule(EmailScheduleCreate):
    id: int
    is_sent: bool

    class Config:
        orm_mode = True
