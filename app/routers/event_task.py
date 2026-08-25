from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.event_task import (
    EventTaskCreate,
    EventTaskResponse,
    EventTaskUpdate
)
from app.services.event_task_service import (
    create_event_task,
    get_event_tasks,
    get_event_task_detail,
    update_event_task,
    delete_event_task,
    assign_event_task,
    search_event_tasks_service,
    paginate_event_tasks_service
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/events", tags=["Event Tasks"])


# 1. Tạo task
@router.post("/{event_id}/event-tasks", response_model=EventTaskResponse)
def create_event_task_endpoint(event_id: int, data: EventTaskCreate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return create_event_task(db, current_user, event_id, data)


# 2. Danh sách task
@router.get("/{event_id}/event-tasks", response_model=list[EventTaskResponse])
def list_event_tasks(event_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return get_event_tasks(db, current_user, event_id)


# 3. Chi tiết task
@router.get("/event-tasks/{task_id}", response_model=EventTaskResponse)
def get_event_task_detail_endpoint(task_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return get_event_task_detail(db, current_user, task_id)


# 4. Cập nhật task
@router.patch("/event-tasks/{task_id}", response_model=EventTaskResponse)
def update_event_task_endpoint(task_id: int, data: EventTaskUpdate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return update_event_task(db, current_user, task_id, data)


# 5. Xóa task
@router.delete("/event-tasks/{task_id}")
def delete_event_task_endpoint(task_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return delete_event_task(db, current_user, task_id)


# 6. Giao việc (assign)
@router.patch("/event-tasks/{task_id}/assign", response_model=EventTaskResponse)
def assign_event_task_endpoint(task_id: int, assignee_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return assign_event_task(db, current_user, task_id, assignee_id)


# 8. Search & filter
@router.get("/{event_id}/event-tasks/search", response_model=list[EventTaskResponse])
def search_event_tasks(event_id: int,status: str | None = None,priority: str | None = None,assignee_id: int | None = None,title: str | None = None,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return search_event_tasks_service(
        db, current_user, event_id, status, priority, assignee_id, title
    )


# 9. Pagination & sort
@router.get("/{event_id}/event-tasks/paginate", response_model=list[EventTaskResponse])
def paginate_event_tasks(event_id: int,page: int = 1,size: int = 10,sort_by: str = "created_at",order: str = "desc",db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return paginate_event_tasks_service(
        db, current_user, event_id, page, size, sort_by, order
    )
