from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from contacts_api.configs.database import get_db
from contacts_api.models import User
from contacts_api.configs.dependencies import create_email_token, verify_email_token
from contacts_api.user import get_current_user, send_email_verification

router = APIRouter()

@router.post("/verify-email/")
def send_verification_email(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified.")
    token = create_email_token(user.email)
    send_email_verification(user.email, token)  
    return {"message": "Verification email sent."}

@router.get("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully."}
