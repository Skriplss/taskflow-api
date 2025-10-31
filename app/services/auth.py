"""
Authentication service for user registration and login.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.exceptions import ConflictException, UnauthorizedException
from app.utils.security import create_access_token, get_password_hash, verify_password


class AuthService:
    """Service for handling authentication operations."""

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Register a new user.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            User: Created user

        Raises:
            ConflictException: If email or username already exists
        """
        # Check if email already exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise ConflictException("Email already registered")

        # Check if username already exists
        result = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        if result.scalar_one_or_none():
            raise ConflictException("Username already taken")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, username: str, password: str
    ) -> tuple[User, str]:
        """
        Authenticate user and generate access token.

        Args:
            db: Database session
            username: Username
            password: Plain text password

        Returns:
            tuple: (User object, JWT access token)

        Raises:
            UnauthorizedException: If credentials are invalid
        """
        # Get user by username
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            raise UnauthorizedException("Incorrect username or password")

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Incorrect username or password")

        # Check if user is active
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")

        # Create access token
        access_token = create_access_token(subject=user.id)

        return user, access_token
