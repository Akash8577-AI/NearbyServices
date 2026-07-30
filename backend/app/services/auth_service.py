from fastapi import HTTPException
from app.models.role import UserRole

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.schemas.user import UserRegister, UserLogin


class AuthService:

    @staticmethod
    async def register(user: UserRegister):

        # Check if email already exists
        existing_user = await UserRepository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        # Hash the password
        hashed_password = hash_password(user.password)

        # Create user object
        new_user = User.create(
    full_name=user.full_name,
    email=user.email,
    phone=user.phone,
    hashed_password=hashed_password,
    role=user.role
)

        # Save to MongoDB
        user_id = await UserRepository.create(new_user)

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    @staticmethod
    async def login(user: UserLogin):

        # Find user by email
        db_user = await UserRepository.get_by_email(user.email)

        # Check if user exists
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(
            user.password,
            db_user["hashed_password"]
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Create JWT Token
        access_token = create_access_token(
            {
                "sub": str(db_user["email"])
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }