from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Driver(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    license_number: str = Field(unique=True)
    license_category: str
    license_expiry: date
    status: str = "available"  # available | on_trip | off_duty | suspended
    safety_score: float = 100
    trip_completed: int = 0