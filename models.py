from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmailSchedule(BaseModel):
    recipient: str
    subject: str
    body: str
    schedule_time: datetime
    recurring: bool
    recurrence_type: Optional[str] = None
    recurrence_value: Optional[str] = None
    id: Optional[int] = None
    is_sent: Optional[bool] = False

