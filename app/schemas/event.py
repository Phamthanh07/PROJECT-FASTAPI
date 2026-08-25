from pydantic import BaseModel,Field
from datetime import datetime

class EventBase(BaseModel):
    name: str 
    description: str | None = None

class EventCreate(EventBase):
   pass

class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class EventResponse(EventBase):
    id: int
    owner_id: int
    created_at: datetime

#Cho phép Pydantic lấy dữ liệu trực tiếp từ object SQLAlchemy Model.
    model_config = {
        "from_attributes": True
    }


