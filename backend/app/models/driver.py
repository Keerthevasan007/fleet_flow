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
    safety_score: Optional[float] = Field(default=100)
    risk_level: str = Field(default="Low")  # Low | Medium | High
    trip_completed: int = Field(default=0)