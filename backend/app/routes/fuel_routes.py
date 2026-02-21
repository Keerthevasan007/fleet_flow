from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.fuel import Fuel
from app.models.vehicle import Vehicle

router = APIRouter(prefix="/fuel", tags=["Fuel Logging"])

# =========================
# ADD FUEL LOG
# =========================
@router.post("/")
def add_fuel_log(log: Fuel, session: Session = Depends(get_session)):

    vehicle = session.get(Vehicle, log.vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    session.add(log)
    session.commit()

    return {"message": "Fuel log added successfully"}


# =========================
# LIST FUEL LOGS
# =========================
@router.get("/")
def get_fuel_logs(session: Session = Depends(get_session)):
    return session.exec(select(Fuel)).all()