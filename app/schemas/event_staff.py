from pydantic import BaseModel
from typing import Optional

class EventStaffBase(BaseModel):
    event_id: int
    user_id: int
    role: str   # OWNER / MEMBER

class EventStaffCreate(EventStaffBase):
    pass

class EventStaffUpdate(BaseModel):
    event_id: int | None = None
    user_id:int | None = None
    role:str | None = None  

class EventStaffResponse(EventStaffBase):
    model_config = {
        "from_attributes": True
    }
