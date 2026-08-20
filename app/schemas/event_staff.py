from pydantic import BaseModel
from typing import Optional

class EventStaffBase(BaseModel):
    event_id: int
    user_id: int
    role: str   # OWNER / MEMBER

class EventStaffCreate(EventStaffBase):
    pass

class EventStaffUpdate(BaseModel):
    event_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[str] = None   # OWNER / MEMBER

class EventStaffResponse(EventStaffBase):
    model_config = {
        "from_attributes": True
    }
