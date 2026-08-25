from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.schemas.event_staff import EventStaffCreate, EventStaffResponse
from app.services.event_service import create_event,get_events,get_event_detail,update_event,delete_event,add_member_to_event,remove_member_from_event,get_event_members 
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.post("/", response_model=EventResponse)
def create_event_api(
    data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = create_event(db, data, current_user)
    return event

@router.get("/", response_model=list[EventResponse]) #nếu k có list thì trả về 1 object
def list_events(
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    events = get_events(db, current_user, search)
    return events

@router.get("/{event_id}", response_model=EventResponse)
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = get_event_detail(db, event_id, current_user)
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event_by_id(
    event_id: int,
    data: EventCreate,   # hoặc EventUpdate nếu bạn có schema riêng
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = update_event(db, event_id, current_user, data)
    return event

@router.delete("/{event_id}")
def delete_event_by_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = delete_event(db, event_id, current_user)
    return result

@router.post("/{event_id}/members", response_model=EventStaffResponse)
def add_member(
    event_id: int,
    data: EventStaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = add_member_to_event(db, event_id, current_user, data)
    return member


@router.delete("/{event_id}/members/{user_id}")
def remove_member(event_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return remove_member_from_event(db, event_id, current_user, user_id)

@router.get("/{event_id}/members", response_model=list[EventStaffResponse])
def list_members(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_event_members(db, event_id, current_user)