from sqlmodel import SQLModel, Field
from typing import Optional

class Vehicle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model: str
    license_plate: str = Field(unique=True, index=True)
    max_capacity: float
    odometer: float = 0
    status: str = "available"  # available | on_trip | in_shop | retired
    acquisition_cost: float
    vehicle_type: str
    region: str