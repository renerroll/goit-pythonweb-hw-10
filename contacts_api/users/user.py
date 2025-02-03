from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from contacts_api.configs.database import get_db
from contacts_api.models import User
from contacts_api.configs.dependencies import verify_email_token
import smtplib
from email.mime.text import MIMEText
from contacts_api.configs.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    email = verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def send_email_verification(email: str, token: str):
    subject = "Verify your email"
    link = f"{settings.FRONTEND_URL}/verify-email/{token}"
    body = f"Click the following link to verify your email: {link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = email

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USERNAME, email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")

