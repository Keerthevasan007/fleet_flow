from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date
from app.db import get_session
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver

router = APIRouter(prefix="/trips", tags=["Trip Management"])

# =============================
# CREATE TRIP
# =============================
@router.post("/")
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

    vehicle.status = "on_trip"
    driver.status = "on_trip"

    session.add(trip)
    session.commit()
    session.refresh(trip)

    return trip


# =============================
# COMPLETE TRIP
# =============================
@router.patch("/{trip_id}/complete")
def complete_trip(trip_id: int, end_odometer: float, revenue: float,
                  session: Session = Depends(get_session)):

    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    if trip.status == "completed":
        raise HTTPException(400, "Trip already completed")

    vehicle = session.get(Vehicle, trip.vehicle_id)
    driver = session.get(Driver, trip.driver_id)

    trip.status = "completed"
    trip.end_odometer = end_odometer
    trip.revenue = revenue

    vehicle.status = "available"
    vehicle.odometer = end_odometer

    driver.status = "available"
    driver.trip_completed += 1

    session.commit()

    return {"message": "Trip completed successfully"}


# =============================
# CANCEL TRIP
# =============================
@router.patch("/{trip_id}/cancel")
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
@router.get("/")
def get_trips(session: Session = Depends(get_session)):
    return session.query(Trip).all()