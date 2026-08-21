from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class EventTask(Base):
    __tablename__ = "event_tasks"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255), nullable=False)
    description = Column(Text)

    assignee_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)

    due_date = Column(DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # QUAN HỆ
    event = relationship("Event", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
