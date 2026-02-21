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

    if log.liters <= 0:
        raise HTTPException(400, "Fuel liters must be greater than 0")

    if log.cost <= 0:
        raise HTTPException(400, "Fuel cost must be greater than 0")

    # Optional: calculate cost_per_liter dynamically
    cost_per_liter = log.cost / log.liters

    session.add(log)
    session.commit()

    return {
        "message": "Fuel log added successfully",
        "vehicle_id": log.vehicle_id,
        "liters": log.liters,
        "total_cost": log.cost,
        "cost_per_liter": round(cost_per_liter, 2)
    }


# =========================
# LIST FUEL LOGS
# =========================
@router.get("/")
def get_fuel_logs(session: Session = Depends(get_session)):
    logs = session.exec(select(Fuel)).all()

    enriched_logs = []
    for log in logs:
        cost_per_liter = (log.cost / log.liters) if log.liters else 0
        enriched_logs.append({
            "id": log.id,
            "vehicle_id": log.vehicle_id,
            "liters": log.liters,
            "total_cost": log.cost,
            "cost_per_liter": round(cost_per_liter, 2)
        })

    return enriched_logs