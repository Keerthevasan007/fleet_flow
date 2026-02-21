from fastapi import Request, HTTPException, Depends

def require_login(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(status_code=401, detail="Login required")

def require_manager(request: Request):
    if request.session.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")

def require_dispatcher_or_manager(request: Request):
    if request.session.get("role") not in ["manager", "dispatcher"]:
        raise HTTPException(status_code=403, detail="Unauthorized")