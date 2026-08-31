"""
MediCore Nexus - Identity & Access Management Models
"""

import enum
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.app.database import Base, TimestampMixin


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "Super Admin"
    HOSPITAL_ADMIN = "Hospital Admin"
    PHARMACY_ADMIN = "Pharmacy Admin"
    DOCTOR = "Doctor"
    PHARMACIST = "Pharmacist"
    PHARMACY_TECH = "Pharmacy Technician"
    NURSE = "Nurse"
    LAB_TECH = "Lab Technician"
    BILLING_OFFICER = "Billing Officer"
    INSURANCE_OFFICER = "Insurance Officer"
    RECEPTIONIST = "Receptionist"
    PATIENT = "Patient"
    SUPPLIER = "Supplier"
    AUDITOR = "Auditor"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mfa_secret: Mapped[str] = mapped_column(String(128), nullable=True)
    
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    hospital_id: Mapped[str] = mapped_column(String(64), nullable=True, index=True)
    department_id: Mapped[str] = mapped_column(String(64), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(512), nullable=True)


class UserSession(Base, TimestampMixin):
    __tablename__ = "user_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), index=True, nullable=False)
    token_jti: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=True)
    device_name: Mapped[str] = mapped_column(String(128), nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SecurityPolicy(Base, TimestampMixin):
    __tablename__ = "security_policies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    policy_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    min_password_length: Mapped[int] = mapped_column(Integer, default=8)
    require_special_char: Mapped[bool] = mapped_column(Boolean, default=True)
    mfa_enforced_roles: Mapped[str] = mapped_column(Text, default="Super Admin,Hospital Admin,Pharmacy Admin")
    session_timeout_minutes: Mapped[int] = mapped_column(Integer, default=120)
