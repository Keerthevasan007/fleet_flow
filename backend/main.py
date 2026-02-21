from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import bcrypt
from sqlmodel import Session, select

from app.db import engine

# Import ALL models
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.maintenance import Maintenance
from app.models.fuel import Fuel
from app.models.user import User

# Import ALL routers
from app.routes.vehicle_routes import router as vehicle_router
from app.routes.driver_routes import router as driver_router
from app.routes.trip_routes import router as trip_router
from app.routes.maintenance_routes import router as maintenance_router
from app.routes.fuel_routes import router as fuel_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.auth_routes import router as auth_router

app = FastAPI(title="Fleet Lifecycle Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="supersecretkey"
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    # Seed demo users (used by the frontend login page)
    with Session(engine) as session:
        demo_users = [
            ("admin@fleetflow.com", "admin123", "manager"),
            ("dispatch@fleetflow.com", "user123", "dispatcher"),
        ]

        for email, password, role in demo_users:
            existing = session.exec(select(User).where(User.email == email)).first()
            if existing:
                continue

            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            session.add(User(email=email, password_hash=password_hash, role=role))

        session.commit()


frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(frontend_dir), html=True), name="ui")

app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(trip_router)
app.include_router(maintenance_router)
app.include_router(fuel_router)
app.include_router(analytics_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Fleet Backend Running"}