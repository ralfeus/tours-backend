from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User, UserRole
from schemas import CurrentUser
from services.auth_service import AuthService

security = HTTPBearer()

# In-memory token blacklist (same as in auth router)
from routers.auth import blacklisted_tokens

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """Get current user from JWT token"""
    token = credentials.credentials
    
    # Check if token is blacklisted
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    
    return AuthService.get_current_user_from_token(db, token)

def require_role(required_roles: list[UserRole]):
    def role_checker(current_user: CurrentUser = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Role-specific dependencies
require_admin = require_role([UserRole.ADMIN])
require_admin_or_leader = require_role([UserRole.ADMIN, UserRole.LEADER])
