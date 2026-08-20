from pydantic import BaseModel

class EventStaffBase(BaseModel):
    event_id: int
    user_id: int
    role: str   # OWNER / MEMBER

class EventStaffCreate(EventStaffBase):
    pass

class EventStaffResponse(EventStaffBase):
    model_config = {
        "from_attributes": True
    }
