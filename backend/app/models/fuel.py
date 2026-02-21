from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Fuel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicle.id")
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id")
    liters: float
    cost: float
    fuel_date: datetime = Field(default_factory=datetime.utcnow)