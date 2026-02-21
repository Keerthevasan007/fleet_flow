from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlmodel import Session, select
 
from app.db import get_session
from app.models.user import User
import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ------------------------
# Register
# ------------------------
@router.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    session: Session = Depends(get_session)
):
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=email,
        password_hash=bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8"),
        role=role
    )

    session.add(user)
    session.commit()

    return {"message": "User registered successfully"}


# ------------------------
# Login
# ------------------------
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["user_id"] = user.id
    request.session["role"] = user.role

    return {
        "message": "Login successful",
        "role": user.role
    }


# ------------------------
# Logout
# ------------------------
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}


# ------------------------
# Current session
# ------------------------
@router.get("/me")
def me(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if not user_id or not role:
        raise HTTPException(status_code=401, detail="Login required")

    return {"user_id": user_id, "role": role}