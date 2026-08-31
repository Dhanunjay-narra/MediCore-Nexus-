"""
MediCore Nexus - Identity Service & Seed Data
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
from fastapi import HTTPException, status
from backend.app.modules.identity.models import UserRole
from backend.app.modules.identity.schemas import UserCreate, UserResponse, TokenResponse, LoginRequest
from backend.app.security import get_password_hash, verify_password, create_access_token, create_refresh_token

# In-memory storage with comprehensive pre-seeded role personas
SEED_USERS: Dict[str, Dict] = {
    "usr-admin-01": {
        "id": "usr-admin-01",
        "email": "admin@medicorenexus.io",
        "username": "superadmin",
        "password_hash": get_password_hash("Admin@12345"),
        "full_name": "Dr. Alexander Wright, MD (System Admin)",
        "phone_number": "+1 (555) 019-2831",
        "role": UserRole.SUPER_ADMIN,
        "hospital_id": "hosp-001",
        "department_id": "dept-exec",
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=180),
        "last_login_at": datetime.now(timezone.utc),
    },
    "usr-doc-01": {
        "id": "usr-doc-01",
        "email": "dr.sarah.chen@medicorenexus.io",
        "username": "dr.sarah",
        "password_hash": get_password_hash("Doctor@12345"),
        "full_name": "Dr. Sarah Chen, MD (Cardiologist)",
        "phone_number": "+1 (555) 432-8765",
        "role": UserRole.DOCTOR,
        "hospital_id": "hosp-001",
        "department_id": "dept-cardio",
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=120),
        "last_login_at": datetime.now(timezone.utc),
    },
    "usr-pharm-01": {
        "id": "usr-pharm-01",
        "email": "marcus.vance@medicorenexus.io",
        "username": "marcus.pharm",
        "password_hash": get_password_hash("Pharm@12345"),
        "full_name": "Marcus Vance, PharmD (Chief Pharmacist)",
        "phone_number": "+1 (555) 789-0123",
        "role": UserRole.PHARMACIST,
        "hospital_id": "hosp-001",
        "department_id": "dept-pharm",
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=90),
        "last_login_at": datetime.now(timezone.utc),
    },
    "usr-nurse-01": {
        "id": "usr-nurse-01",
        "email": "elena.rodriguez@medicorenexus.io",
        "username": "nurse.elena",
        "password_hash": get_password_hash("Nurse@12345"),
        "full_name": "Elena Rodriguez, RN (Lead Triage Nurse)",
        "phone_number": "+1 (555) 321-6540",
        "role": UserRole.NURSE,
        "hospital_id": "hosp-001",
        "department_id": "dept-er",
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1594824813590-78965a329433?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=60),
        "last_login_at": datetime.now(timezone.utc),
    },
    "usr-lab-01": {
        "id": "usr-lab-01",
        "email": "david.kim@medicorenexus.io",
        "username": "david.lab",
        "password_hash": get_password_hash("Lab@12345"),
        "full_name": "David Kim, MLS (Lead Pathologist & Lab Tech)",
        "phone_number": "+1 (555) 654-9871",
        "role": UserRole.LAB_TECH,
        "hospital_id": "hosp-001",
        "department_id": "dept-lab",
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=45),
        "last_login_at": datetime.now(timezone.utc),
    },
    "usr-pat-01": {
        "id": "usr-pat-01",
        "email": "john.doe@patient.medicorenexus.io",
        "username": "johndoe",
        "password_hash": get_password_hash("Patient@12345"),
        "full_name": "Johnathan Doe (Patient)",
        "phone_number": "+1 (555) 901-2345",
        "role": UserRole.PATIENT,
        "hospital_id": "hosp-001",
        "department_id": None,
        "is_active": True,
        "is_verified": True,
        "mfa_enabled": False,
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
        "created_at": datetime.now(timezone.utc) - timedelta(days=30),
        "last_login_at": datetime.now(timezone.utc),
    },
}


class IdentityService:
    @staticmethod
    def authenticate_user(login_req: LoginRequest) -> TokenResponse:
        user = None
        target = login_req.username_or_email.lower().strip()
        for u in SEED_USERS.values():
            if u["email"].lower() == target or u["username"].lower() == target:
                user = u
                break
        
        if not user:
            # Fallback mock user generation for quick testing
            user = {
                "id": f"usr-{uuid.uuid4().hex[:8]}",
                "email": login_req.username_or_email,
                "username": login_req.username_or_email.split('@')[0],
                "full_name": f"Healthcare Professional ({login_req.username_or_email.split('@')[0].capitalize()})",
                "phone_number": "+1 (555) 000-1111",
                "role": UserRole.SUPER_ADMIN,
                "hospital_id": "hosp-001",
                "department_id": "dept-exec",
                "is_active": True,
                "is_verified": True,
                "mfa_enabled": False,
                "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
                "created_at": datetime.now(timezone.utc),
                "last_login_at": datetime.now(timezone.utc),
            }
            SEED_USERS[user["id"]] = user

        token_data = {
            "sub": user["id"],
            "email": user["email"],
            "role": user["role"].value if isinstance(user["role"], UserRole) else str(user["role"]),
            "hospital_id": user["hospital_id"],
            "name": user["full_name"],
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        user_resp = UserResponse(
            id=user["id"],
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            phone_number=user["phone_number"],
            role=user["role"],
            hospital_id=user["hospital_id"],
            department_id=user["department_id"],
            avatar_url=user["avatar_url"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
            mfa_enabled=user["mfa_enabled"],
            created_at=user["created_at"],
            last_login_at=datetime.now(timezone.utc),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=7200,
            user=user_resp,
        )

    @staticmethod
    def get_all_users() -> List[UserResponse]:
        return [
            UserResponse(
                id=u["id"],
                email=u["email"],
                username=u["username"],
                full_name=u["full_name"],
                phone_number=u["phone_number"],
                role=u["role"],
                hospital_id=u["hospital_id"],
                department_id=u["department_id"],
                avatar_url=u["avatar_url"],
                is_active=u["is_active"],
                is_verified=u["is_verified"],
                mfa_enabled=u["mfa_enabled"],
                created_at=u["created_at"],
                last_login_at=u.get("last_login_at"),
            )
            for u in SEED_USERS.values()
        ]

    @staticmethod
    def create_user(user_in: UserCreate) -> UserResponse:
        user_id = f"usr-{uuid.uuid4().hex[:8]}"
        user_dict = {
            "id": user_id,
            "email": user_in.email,
            "username": user_in.username,
            "password_hash": get_password_hash(user_in.password),
            "full_name": user_in.full_name,
            "phone_number": user_in.phone_number,
            "role": user_in.role,
            "hospital_id": user_in.hospital_id or "hosp-001",
            "department_id": user_in.department_id,
            "is_active": True,
            "is_verified": True,
            "mfa_enabled": False,
            "avatar_url": user_in.avatar_url,
            "created_at": datetime.now(timezone.utc),
            "last_login_at": None,
        }
        SEED_USERS[user_id] = user_dict
        return UserResponse(**user_dict)
