import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from contacts_api.configs.config import settings

# Secret key and encryption algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24  

def create_email_token(email: str) -> str:
    """Generates a JWT token for email verification."""
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_email_token(token: str) -> str:
    """Decrypts a JWT token and returns an email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
