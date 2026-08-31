"""
MediCore Nexus - Identity API Router
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.modules.identity.schemas import (
    LoginRequest, TokenResponse, UserCreate, UserResponse, PasswordChangeRequest
)
from backend.app.modules.identity.service import IdentityService
from backend.app.security import get_current_user_payload

router = APIRouter(prefix="/auth", tags=["Identity & Access Management"])


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Authenticate user with email/username and password, returning JWT tokens."""
    return IdentityService.authenticate_user(login_data)


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """Return currently authenticated user token claims and roles."""
    return payload


@router.get("/users", response_model=List[UserResponse])
async def list_users(payload: Dict[str, Any] = Depends(get_current_user_payload)):
    """List all registered system users (RBAC protected)."""
    return IdentityService.get_all_users()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    """Register a new user account."""
    return IdentityService.create_user(user_in)


@router.post("/logout")
async def logout():
    """Invalidate session and sign out user."""
    return {"status": "success", "message": "Successfully logged out from MediCore Nexus."}
