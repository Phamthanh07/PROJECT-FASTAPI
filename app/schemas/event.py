from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    description: str | None = None

class EventCreate(EventBase):
    owner_id: int

class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class EventResponse(EventBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
