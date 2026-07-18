from datetime import datetime


class User:
    @staticmethod
    def create(
        full_name: str,
        email: str,
        phone: str,
        hashed_password: str
    ):
        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            # "password": hashed_password,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow()
        }