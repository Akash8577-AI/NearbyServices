from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.schemas.user import UserRegister


class AuthService:

    @staticmethod
    async def register(user: UserRegister):

        existing_user = await UserRepository.get_by_email(user.email)

        if existing_user:
            raise Exception("Email already exists")

        hashed_password = hash_password(user.password)

        new_user = User.create(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password
        )

        user_id = await UserRepository.create(new_user)

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }