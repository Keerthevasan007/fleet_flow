from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.vehicle import Vehicle

router = APIRouter(prefix="/vehicles", tags=["Vehicle Registry"])

@router.post("/")
def create_vehicle(vehicle: Vehicle, session: Session = Depends(get_session)):
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

@router.get("/")
def get_vehicles(session: Session = Depends(get_session)):
    return session.exec(select(Vehicle)).all()

@router.get("/available")
def get_available_vehicles(session: Session = Depends(get_session)):
    return session.exec(
        select(Vehicle).where(Vehicle.status == "available")
    ).all()

@router.patch("/{vehicle_id}/retire")
def retire_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")
    vehicle.status = "retired"
    session.commit()
    return {"message": "Vehicle retired"}