from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # QUAN HỆ
    owner = relationship("User", back_populates="events")
    staff = relationship("EventStaff", back_populates="event")
    tasks = relationship("EventTask", back_populates="event")


from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class EventStaff(Base):
    __tablename__ = "event_staff"

    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    role = Column(String(50), nullable=False)

    # QUAN HỆ
    event = relationship("Event", back_populates="staff")
    user = relationship("User", back_populates="event_memberships")
