from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.driver import Driver

router = APIRouter(prefix="/drivers", tags=["Driver Management"])

@router.post("/")
def create_driver(driver: Driver, session: Session = Depends(get_session)):
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return driver

@router.get("/")
def get_drivers(session: Session = Depends(get_session)):
    return session.exec(select(Driver)).all()

@router.get("/available")
def get_available_drivers(session: Session = Depends(get_session)):
    return session.exec(
        select(Driver).where(Driver.status == "available")
    ).all()

@router.patch("/{driver_id}/suspend")
def suspend_driver(driver_id: int, session: Session = Depends(get_session)):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(404, "Driver not found")
    driver.status = "suspended"
    session.commit()
    return {"message": "Driver suspended"}

@router.patch("/{driver_id}/status")
def change_driver_status(driver_id: int, status: str, session: Session = Depends(get_session)):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(404, "Driver not found")
    driver.status = status
    session.commit()
    return {"message": f"Driver status updated to {status}"}