from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.maintenance import Maintenance
from app.models.vehicle import Vehicle

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

# =========================
# ADD MAINTENANCE
# =========================
@router.post("/")
def add_maintenance(log: Maintenance, session: Session = Depends(get_session)):

    vehicle = session.get(Vehicle, log.vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    # Auto move vehicle to in_shop
    vehicle.status = "in_shop"

    session.add(log)
    session.commit()

    return {"message": "Maintenance logged. Vehicle moved to in_shop."}


# =========================
# LIST MAINTENANCE
# =========================
@router.get("/")
def get_maintenance(session: Session = Depends(get_session)):
    return session.exec(select(Maintenance)).all()