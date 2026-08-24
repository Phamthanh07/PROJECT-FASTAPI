from sqlalchemy.orm import Session
from app.models.event import Event, EventStaff
from app.models.event_task import EventTask
from app.schemas.event import EventCreate, EventResponse
from app.models.user import User
from fastapi import HTTPException, status

def create_event(db: Session, data: EventCreate, current_user: User):
    # Validate tên sự kiện
    if not data.name or data.name.strip() == "":
        raise ValueError("Tên sự kiện không được để trống")

    # Tạo sự kiện
    event = Event(
        name=data.name,
        description=data.description,
        owner_id=current_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Gán OWNER vào event_staff
    owner = EventStaff(
        event_id=event.id,
        user_id=current_user.id,
        role="OWNER"
    )
    db.add(owner)
    db.commit()

    return event

def get_events(db: Session, current_user: User, search: str | None = None):
    # Query event mà user là OWNER
    owner_events = (
        db.query(Event)
        .filter(Event.owner_id == current_user.id)
    )

    # Query event mà user là MEMBER
    member_events = (
        db.query(Event)
        .join(EventStaff, EventStaff.event_id == Event.id)
        .filter(EventStaff.user_id == current_user.id)
    )

    # UNION 2 query lại
    events = owner_events.union(member_events)

    # Search theo tên sự kiện (LIKE)
    if search:
        events = events.filter(Event.name.like(f"%{search}%"))

    return events.all()

def get_event_detail(db: Session, event_id: int, current_user: User):
    # 1) Kiểm tra event có tồn tại không
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 2) Kiểm tra quyền (OWNER hoặc MEMBER)
    is_member = db.query(EventStaff).filter(EventStaff.event_id == event_id, EventStaff.user_id == current_user.id).first()
    allowed = event.owner_id == current_user.id or is_member

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this event"
        )

    return event

def update_event(db: Session, event_id: int, current_user: User, data):
    # 1) Kiểm tra event tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 2) Kiểm tra quyền OWNER
    if event.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner can update this event"
        )

    # 3) Cập nhật dữ liệu
    event.name = data.name
    event.description = data.description

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int, current_user: User):
    # 1) Kiểm tra event tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 2) Kiểm tra quyền OWNER
    if event.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner can delete this event"
        )

    # 3) Xóa event_staff
    db.query(EventStaff).filter(EventStaff.event_id == event_id).delete()

    # 4) Xóa event_tasks
    db.query(EventTask).filter(EventTask.event_id == event_id).delete()

    # 5) Xóa event
    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}


def add_member_to_event(db: Session, event_id: int, current_user: User, data):
    # 1) Kiểm tra event tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 2) Chỉ OWNER được thêm member
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can add members")

    # 3) Kiểm tra user được thêm có tồn tại
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 4) Không cho thêm owner
    if data.user_id == event.owner_id:
        raise HTTPException(status_code=400, detail="Owner is already a member")

    # 5) Kiểm tra user đã là member chưa
    exists = db.query(EventStaff).filter(
        EventStaff.event_id == event_id,
        EventStaff.user_id == data.user_id
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Member already exists")

    # 6) Thêm member mới
    new_member = EventStaff(
        event_id=event_id,
        user_id=data.user_id,
        role=data.role
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


def remove_member_from_event(db: Session, event_id: int, current_user: User, user_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can remove members")

    if user_id == event.owner_id:
        raise HTTPException(status_code=400, detail="Cannot remove owner")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event_id,
        EventStaff.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(status_code=400, detail="User is not a member of this event")

    db.delete(member)
    db.commit()

    return {"message": "Member removed successfully"}

def get_event_members(db: Session, event_id: int, current_user: User):
    # 1) Kiểm tra event tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 2) Kiểm tra quyền xem danh sách
    # Owner được xem
    if current_user.id == event.owner_id:
        pass
    else:
        # Member được xem
        is_member = db.query(EventStaff).filter(
            EventStaff.event_id == event_id,
            EventStaff.user_id == current_user.id
        ).first()

        if not is_member:
            raise HTTPException(status_code=403, detail="You do not have permission to view members")

    # 3) Lấy danh sách member
    members = db.query(EventStaff).filter(EventStaff.event_id == event_id).all()

    return members