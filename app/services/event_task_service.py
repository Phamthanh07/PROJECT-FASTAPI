from sqlalchemy.orm import Session
from app.models.event import Event, EventStaff
from app.models.event_task import EventTask
from app.core.exceptions import not_found, forbidden, bad_request
from app.schemas.event_task import EventTaskUpdate

VALID_PRIORITY = {"LOW", "MEDIUM", "HIGH"}
VALID_STATUS = {"TODO", "IN_PROGRESS", "DONE"}


# 1. Tạo task
def create_event_task(db: Session, current_user, event_id: int, data):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại", event_id)

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    if data.priority not in VALID_PRIORITY:
        bad_request("Priority không hợp lệ")

    if data.assignee_id:
        assignee_member = db.query(EventStaff).filter(
            EventStaff.event_id == event.id,
            EventStaff.user_id == data.assignee_id
        ).first()

        if not assignee_member and event.owner_id != data.assignee_id:
            forbidden("Không thể giao việc cho người ngoài sự kiện")

    new_task = EventTask(
        event_id=event_id,
        title=data.title,
        description=data.description,
        status="TODO",
        priority=data.priority,
        due_date=data.due_date,
        assignee_id=data.assignee_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# 2. Danh sách task
def get_event_tasks(db: Session, current_user, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    return db.query(EventTask).filter(EventTask.event_id == event_id).all()


# 3. Chi tiết task
def get_event_task_detail(db: Session, current_user, task_id: int):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        not_found("Công việc sự kiện không tồn tại")

    event = db.query(Event).filter(Event.id == task.event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    return task


# 4. Cập nhật task
def update_event_task(db: Session, current_user, task_id: int, data: EventTaskUpdate):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        not_found("Công việc sự kiện không tồn tại")

    event = db.query(Event).filter(Event.id == task.event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    update_data = data.model_dump(exclude_unset=True)

    #khi không có exclude Và khi bạn update, nó sẽ ghi đè tất cả thành None bị xóa sạch dữ liệu.Vậy nên exclude_unset=True là bắt buộc.

    if "priority" in update_data and update_data["priority"] not in VALID_PRIORITY:
        bad_request("Priority không hợp lệ")

    if "status" in update_data and update_data["status"] not in VALID_STATUS:
        bad_request("Status không hợp lệ")

    if "assignee_id" in update_data:
        assignee_id = update_data["assignee_id"]
        if assignee_id is not None:
            assignee_member = db.query(EventStaff).filter(
                EventStaff.event_id == event.id,
                EventStaff.user_id == assignee_id
            ).first()

            if not assignee_member and event.owner_id != assignee_id:
                bad_request("Người được giao phải thuộc sự kiện")

    for field, value in update_data.items():
        setattr(task, field, value)

        #setattr ghi tắt của task.field = value

    db.commit()
    db.refresh(task)
    return task


# 5. Xóa task
def delete_event_task(db: Session, current_user, task_id: int):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        not_found("Công việc sự kiện không tồn tại")

    event = db.query(Event).filter(Event.id == task.event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    db.delete(task)
    db.commit()
    return {"message": "Xóa công việc sự kiện thành công"}


# 6. Giao việc
def assign_event_task(db: Session, current_user, task_id: int, assignee_id: int):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        not_found("Task không tồn tại")

    event = db.query(Event).filter(Event.id == task.event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    if event.owner_id != current_user.id:
        forbidden("Chỉ chủ sự kiện mới được giao việc")

    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == assignee_id
    ).first()

    if not member and assignee_id != event.owner_id:
        bad_request("Người được giao phải thuộc sự kiện")

    task.assignee_id = assignee_id
    db.commit()
    db.refresh(task)
    return task


# 8. Search & filter
def list_event_tasks_service(
    db: Session,
    current_user,
    event_id: int,
    status: str | None,
    priority: str | None,
    assignee_id: int | None,
    title: str | None,
    page: int,
    size: int,
    sort_by: str,
    order: str
):
    # 1. Kiểm tra event tồn tại
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        not_found("Sự kiện không tồn tại")

    # 2. Kiểm tra user thuộc event
    member = db.query(EventStaff).filter(
        EventStaff.event_id == event.id,
        EventStaff.user_id == current_user.id
    ).first()

    if not member and event.owner_id != current_user.id:
        forbidden("Bạn không thuộc sự kiện này")

    # 3. Base query
    query = db.query(EventTask).filter(EventTask.event_id == event_id)
    #Lấy tất cả task thuộc event

    # 4. Filter
    if status:
        query = query.filter(EventTask.status == status)

    if priority:
        query = query.filter(EventTask.priority == priority)

    if assignee_id:
        query = query.filter(EventTask.assignee_id == assignee_id)

    if title:
        query = query.filter(EventTask.title.like(f"%{title}%"))

    # 5. Sort
    sort_column = getattr(EventTask, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # 6. Pagination
    offset = (page - 1) * size
    tasks = query.offset(offset).limit(size).all()

    return tasks
