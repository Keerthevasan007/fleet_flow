from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db import get_session
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.fuel import Fuel
from app.models.maintenance import Maintenance

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# =========================
# DASHBOARD KPIs
# =========================
@router.get("/dashboard")
def dashboard(session: Session = Depends(get_session)):

    vehicles = session.exec(select(Vehicle)).all()
    trips = session.exec(select(Trip)).all()

    total_vehicles = len(vehicles)
    active_vehicles = len([v for v in vehicles if v.status == "on_trip"])
    in_shop = len([v for v in vehicles if v.status == "in_shop"])
    pending_trips = len([t for t in trips if t.status == "draft"])

    utilization_rate = (active_vehicles / total_vehicles) if total_vehicles else 0

    return {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "in_shop": in_shop,
        "pending_trips": pending_trips,
        "utilization_rate": utilization_rate
    }


# =========================
# VEHICLE OPERATIONAL COST
# =========================
@router.get("/vehicle/{vehicle_id}/cost")
def vehicle_operational_cost(vehicle_id: int, session: Session = Depends(get_session)):

    fuel_logs = session.exec(
        select(Fuel).where(Fuel.vehicle_id == vehicle_id)
    ).all()

    maintenance_logs = session.exec(
        select(Maintenance).where(Maintenance.vehicle_id == vehicle_id)
    ).all()

    total_fuel = sum(f.cost for f in fuel_logs)
    total_maintenance = sum(m.cost for m in maintenance_logs)

    return {
        "vehicle_id": vehicle_id,
        "fuel_cost": total_fuel,
        "maintenance_cost": total_maintenance,
        "total_operational_cost": total_fuel + total_maintenance
    }


# =========================
# FUEL EFFICIENCY (km/L)
# =========================
@router.get("/vehicle/{vehicle_id}/efficiency")
def fuel_efficiency(vehicle_id: int, session: Session = Depends(get_session)):

    trips = session.exec(
        select(Trip).where(Trip.vehicle_id == vehicle_id, Trip.status == "completed")
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

    return {
        "vehicle_id": vehicle_id,
        "total_km": total_km,
        "total_liters": total_liters,
        "fuel_efficiency_km_per_l": efficiency
    }


# =========================
# ROI CALCULATION
# =========================
@router.get("/vehicle/{vehicle_id}/roi")
def vehicle_roi(vehicle_id: int, session: Session = Depends(get_session)):

    vehicle = session.get(Vehicle, vehicle_id)

    trips = session.exec(
        select(Trip).where(Trip.vehicle_id == vehicle_id)
    ).all()

    fuel_logs = session.exec(
        select(Fuel).where(Fuel.vehicle_id == vehicle_id)
    ).all()

    maintenance_logs = session.exec(
        select(Maintenance).where(Maintenance.vehicle_id == vehicle_id)
    ).all()

    total_revenue = sum(t.revenue for t in trips)
    total_cost = sum(f.cost for f in fuel_logs) + sum(m.cost for m in maintenance_logs)

    roi = 0
    if vehicle and vehicle.acquisition_cost > 0:
        roi = (total_revenue - total_cost) / vehicle.acquisition_cost

    return {
        "vehicle_id": vehicle_id,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "roi": roi
    }