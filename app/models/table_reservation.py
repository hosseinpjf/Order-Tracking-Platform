from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum
from app.db.base import Base


class ReservationStatus(enum.Enum):
    pending = "pending"       # رزرو ثبت شده ولی هنوز تایید نشده
    confirmed = "confirmed"   # رزرو تایید شده
    completed = "completed"   # میز آزاد شده و تحویل کاربر داده شده
    cancelled = "cancelled"   # کاربر یا ادمین رزرو را لغو کرده
    rejected = "rejected"     # ادمین رزرو را رد کرده


class TableReservation(Base):
    __tablename__ = "table_reservations"

    id = Column(String, primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    table_id = Column(String, ForeignKey("tables.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    guests_count = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.pending)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    table = relationship("Table", back_populates="reservations")
    user = relationship("User", back_populates="reservations")