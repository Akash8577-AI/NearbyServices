from datetime import datetime


class Provider:

    @staticmethod
    def create(
        service_id: str,
        full_name: str,
        phone: str,
        email: str,
        experience: int,
        address: str,
        is_available: bool
    ):
        return {
            "service_id": service_id,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "experience": experience,
            "address": address,
            "is_available": is_available,
            "created_at": datetime.utcnow()
        }