from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.vehicle import Vehicle
from fastapi import Depends
from app.dependencies import require_manager, require_dispatcher_or_manager
from sqlmodel import select
from app.models.trip import Trip
from app.models.fuel import Fuel

router = APIRouter(prefix="/vehicles", tags=["Vehicle Registry"])

@router.post("/", dependencies=[Depends(require_manager)])
def create_vehicle(vehicle: Vehicle, session: Session = Depends(get_session)):
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

@router.get("/", dependencies=[Depends(require_dispatcher_or_manager)])
def get_vehicles(session: Session = Depends(get_session)):
    return session.exec(select(Vehicle)).all()

@router.get("/available", dependencies=[Depends(require_dispatcher_or_manager)])
def get_available_vehicles(session: Session = Depends(get_session)):
    return session.exec(
        select(Vehicle).where(Vehicle.status == "available")
    ).all()

@router.patch("/{vehicle_id}/retire", dependencies=[Depends(require_manager)])
def retire_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")
    vehicle.status = "retired"
    session.commit()
    return {"message": "Vehicle retired"}

# =========================
# VEHICLE GRADE
# =========================
@router.get("/{vehicle_id}/grade")
def vehicle_grade(vehicle_id: int, session: Session = Depends(get_session)):

    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    trips = session.exec(
        select(Trip).where(
            Trip.vehicle_id == vehicle_id,
            Trip.status == "completed"
        )
    ).all()

    fuel_logs = session.exec(
        select(Fuel).where(Fuel.vehicle_id == vehicle_id)
    ).all()

    total_km = 0
    for trip in trips:
        if trip.end_odometer and trip.start_odometer:
            total_km += (trip.end_odometer - trip.start_odometer)

    total_liters = sum(f.liters for f in fuel_logs)

    efficiency = (total_km / total_liters) if total_liters else 0

    # ---- Grading Logic ----
    if total_liters == 0:
        grade = "N/A"
    elif efficiency >= 12:
        grade = "A"
    elif efficiency >= 9:
        grade = "B"
    elif efficiency >= 7:
        grade = "C"
    else:
        grade = "D"

    return {
        "vehicle_id": vehicle_id,
        "total_km": total_km,
        "total_liters": total_liters,
        "efficiency_km_per_l": round(efficiency, 2),
        "grade": grade
    }