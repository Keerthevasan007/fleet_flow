from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Maintenance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicle.id")
    description: str
    cost: float
    service_date: datetime = Field(default_factory=datetime.utcnow)