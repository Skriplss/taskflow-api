"""
Authentication API endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserLogin
from app.services.auth import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email, username, and password.",
)
async def register(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Register a new user.

    - **email**: Valid email address (must be unique)
    - **username**: Username (3-50 characters, must be unique)
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    user = await AuthService.register_user(db, user_data)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate user and receive JWT access token.",
)
async def login(
    credentials: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Login with username and password.

    - **username**: Your username
    - **password**: Your password

    Returns JWT access token to use for authenticated requests.
    """
    user, access_token = await AuthService.authenticate_user(
        db, credentials.username, credentials.password
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user",
    description="Get information about the currently authenticated user.",
)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get current user information.

    Requires authentication (Bearer token in Authorization header).
    """
    return current_user
