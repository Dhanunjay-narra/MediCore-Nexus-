"""
MediCore Nexus - Identity & Access Pydantic Schemas
"""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from backend.app.modules.identity.models import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=150)
    phone_number: Optional[str] = None
    role: UserRole = UserRole.PATIENT
    hospital_id: Optional[str] = None
    department_id: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    hospital_id: Optional[str] = None
    department_id: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    mfa_enabled: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username_or_email: str
    password: str
    device_name: Optional[str] = "Web Browser"
    mfa_otp: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MFASetupResponse(BaseModel):
    secret: str
    qr_uri: str
    message: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
