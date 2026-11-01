import time
import hashlib
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ADMIN_PASSWORD
from app.database import get_db, get_setting

ALGORITHM = "HS256"
COOKIE_NAME = "fhh_session"

def hash_password(password: str) -> str:
    """Hash password using sha256 with secret salt for simplicity and speed."""
    salted = f"{SECRET_KEY}:{password}"
    return hashlib.sha256(salted.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_in_seconds: int = 86400 * 30) -> str:
    to_encode = data.copy()
    expire = time.time() + expires_in_seconds
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        # Check Authorization header if API call
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

def require_auth(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        if request.url.path.startswith("/api/"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        return None
    return user
