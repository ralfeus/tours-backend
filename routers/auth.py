from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas import (
    LoginRequest, 
    SignupRequest, 
    AuthResponse, 
    MessageResponse, 
    CurrentUser
)
from services.auth_service import AuthService

router = APIRouter()
security = HTTPBearer()

# In-memory token blacklist (in production, use Redis or database)
blacklisted_tokens = set()

@router.post("/signup", response_model=AuthResponse)
async def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        # Create user
        user = AuthService.create_user(db, user_data)
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = AuthService.create_access_token(
            data={
                "sub": user.username,
                "id": user.id,
                "role": user.role.name,
            }, 
            expires_delta=access_token_expires
        )
        
        # Return user info and token
        current_user = CurrentUser(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active
        )
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=current_user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token"""
    # Authenticate user
    user = AuthService.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "role": user.role.name,
        }, 
        expires_delta=access_token_expires
    )
    
    # Return user info and token
    current_user = CurrentUser(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=current_user
    )

@router.post("/logout", response_model=MessageResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Logout user by blacklisting the token"""
    token = credentials.credentials
    
    # Verify token is valid before blacklisting
    try:
        AuthService.verify_token(token)
        blacklisted_tokens.add(token)
        return MessageResponse(message="Successfully logged out")
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.get("/me", response_model=CurrentUser)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    token = credentials.credentials
    
    # Check if token is blacklisted
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    
    return AuthService.get_current_user_from_token(db, token)
