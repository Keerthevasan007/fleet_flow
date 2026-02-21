from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    vehicle_id: int = Field(foreign_key="vehicle.id")
    driver_id: int = Field(foreign_key="driver.id")

    cargo_weight: float
    origin: str
    destination: str

    status: str = "draft"  # draft | dispatched | completed | cancelled

    start_odometer: float
    end_odometer: Optional[float] = None

    revenue: float = 0

    # 🔥 Behavioural Metrics (For Safety Scoring)
    overspeed_count: int = Field(default=0)
    harsh_brake_count: int = Field(default=0)
    accident_reported: bool = Field(default=False)
    is_night_trip: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)