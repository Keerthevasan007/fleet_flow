from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.db import get_session
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        password_hash=pwd_context.hash(password),
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

    if not user or not pwd_context.verify(password, user.password_hash):
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