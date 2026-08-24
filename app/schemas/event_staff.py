from pydantic import BaseModel

class EventStaffBase(BaseModel):
    event_id: int
    user_id: int
    role: str   

class EventStaffCreate(BaseModel):
    user_id: int
    role: str

class EventStaffUpdate(BaseModel):
    event_id: int | None = None
    user_id:int | None = None
    role:str | None = None  

class EventStaffResponse(EventStaffBase):
    model_config = {
        "from_attributes": True
    }
