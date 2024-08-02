from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmailScheduleCreate(BaseModel):
    recipient: str
    subject: str
    body: str
    schedule_time: datetime
    recurring: bool
    recurrence_type: Optional[str] = None
    recurrence_value: Optional[str] = None

class EmailSchedule(EmailScheduleCreate):
    id: int
    is_sent: bool = False

    class Config:
        from_attributes = True  # This replaces orm_mode=True

class DeleteResponse(BaseModel):
    detail: str