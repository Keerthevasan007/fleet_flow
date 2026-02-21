from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date
from app.db import get_session
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.dependencies import require_dispatcher_or_manager
import random

router = APIRouter(prefix="/trips", tags=["Trip Management"])

# =============================
# CREATE TRIP
# =============================
@router.post("/", dependencies=[Depends(require_dispatcher_or_manager)])
def create_trip(trip: Trip, session: Session = Depends(get_session)):

    vehicle = session.get(Vehicle, trip.vehicle_id)
    driver = session.get(Driver, trip.driver_id)

    if not vehicle or not driver:
        raise HTTPException(404, "Vehicle or Driver not found")

    if vehicle.status != "available":
        raise HTTPException(400, "Vehicle not available")

    if driver.status != "available":
        raise HTTPException(400, "Driver not available")

    if driver.license_expiry < date.today():
        raise HTTPException(400, "Driver license expired")

    if trip.cargo_weight > vehicle.max_capacity:
        raise HTTPException(400, "Cargo exceeds vehicle capacity")

    trip.status = "dispatched"

    vehicle.status = "on_trip"
    driver.status = "on_trip"

    session.add(trip)
    session.commit()
    session.refresh(trip)

    return trip


# =============================
# COMPLETE TRIP
# =============================
@router.patch("/{trip_id}/complete", dependencies=[Depends(require_dispatcher_or_manager)])
def complete_trip(
    trip_id: int,
    end_odometer: float,
    revenue: float,
    session: Session = Depends(get_session)
):

    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    if trip.status == "completed":
        raise HTTPException(400, "Trip already completed")

    vehicle = session.get(Vehicle, trip.vehicle_id)
    driver = session.get(Driver, trip.driver_id)

    # ---------------------------
    # BASIC VALIDATION
    # ---------------------------
    if end_odometer < trip.start_odometer:
        raise HTTPException(400, "End odometer cannot be less than start")

    # ---------------------------
    # COMPLETE TRIP DATA
    # ---------------------------
    trip.status = "completed"
    trip.end_odometer = end_odometer
    trip.revenue = revenue

    distance = end_odometer - trip.start_odometer

    # ---------------------------
    # 🔥 RANDOM BEHAVIOUR SIMULATION
    # ---------------------------

    # Overspeed depends on distance (more realistic)
    if distance > 300:
        trip.overspeed_count = random.randint(2, 7)
    else:
        trip.overspeed_count = random.randint(0, 3)

    trip.harsh_brake_count = random.randint(0, 4)

    # 10% accident probability
    trip.accident_reported = random.random() < 0.1

    # Night detection based on created_at time
    hour = trip.created_at.hour
    trip.is_night_trip = hour >= 22 or hour <= 5

    # ---------------------------
    # 🔥 UPDATE DRIVER SAFETY SCORE
    # ---------------------------

    score = driver.safety_score or 100

    score -= trip.overspeed_count * 2
    score -= trip.harsh_brake_count * 1.5

    if trip.accident_reported:
        score -= 20

    if trip.is_night_trip:
        score -= 3

    driver.safety_score = max(score, 0)

    # Risk classification
    if driver.safety_score >= 75:
        driver.risk_level = "Low"
    elif driver.safety_score >= 50:
        driver.risk_level = "Medium"
    else:
        driver.risk_level = "High"

    # ---------------------------
    # UPDATE OTHER FIELDS
    # ---------------------------
    driver.status = "available"
    driver.trip_completed += 1

    vehicle.status = "available"
    vehicle.odometer = end_odometer

    session.add(trip)
    session.add(driver)
    session.add(vehicle)
    session.commit()

    return {
        "message": "Trip completed successfully",
        "overspeed_count": trip.overspeed_count,
        "harsh_brake_count": trip.harsh_brake_count,
        "accident_reported": trip.accident_reported,
        "new_safety_score": driver.safety_score,
        "risk_level": driver.risk_level
    }


# =============================
# CANCEL TRIP
# =============================
@router.patch("/{trip_id}/cancel", dependencies=[Depends(require_dispatcher_or_manager)])
def cancel_trip(trip_id: int, session: Session = Depends(get_session)):

    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    vehicle = session.get(Vehicle, trip.vehicle_id)
    driver = session.get(Driver, trip.driver_id)

    trip.status = "cancelled"

    if vehicle:
        vehicle.status = "available"

    if driver:
        driver.status = "available"

    session.commit()

    return {"message": "Trip cancelled"}


# =============================
# LIST TRIPS
# =============================
@router.get("/", dependencies=[Depends(require_dispatcher_or_manager)])
def get_trips(session: Session = Depends(get_session)):
    return session.query(Trip).all()