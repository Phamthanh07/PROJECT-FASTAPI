from pydantic import BaseModel
from datetime import datetime

class EventTaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str
    priority: str
    due_date: datetime | None = None

class EventTaskCreate(EventTaskBase):
    event_id: int
    assignee_id: int | None = None

class EventTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None

class EventTaskResponse(EventTaskBase):
    id: int
    event_id: int
    assignee_id: int | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
