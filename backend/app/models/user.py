from datetime import datetime
from app.models.role import UserRole


class User:
    @staticmethod
    def create(
        full_name: str,
        email: str,
        phone: str,
        hashed_password: str,
        role: UserRole = UserRole.CUSTOMER
    ):
        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "hashed_password": hashed_password,
            "role": role,
            "created_at": datetime.utcnow()
        }