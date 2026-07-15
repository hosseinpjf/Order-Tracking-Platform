from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
from app.models.table import TableTags, TableStatus
from app.models.table_reservation import ReservationStatus
from app.schemas.table import OutTable
from app.schemas.table_reservation import OutReservation
from app.schemas.user import OutUser


class OutFullTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    number: int
    image: str
    capacity: int
    location: str
    status: TableStatus
    tags: List[TableTags]
    reservations: list[OutReservation]

class OutFullReservation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    table_id: str
    table_number: int
    user_id: str
    start_time: datetime
    end_time: datetime
    guests_count: int
    status: ReservationStatus
    created_at: datetime
    table: OutTable
    user: OutUser