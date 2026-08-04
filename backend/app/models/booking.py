from datetime import datetime


class Booking:

    @staticmethod
    def create(
        customer_id: str,
        provider_id: str,
        service_id: str,
        booking_date: str,
        booking_time: str,
        address: str,
        status: str = "Pending"
    ):
        return {
            "customer_id": customer_id,
            "provider_id": provider_id,
            "service_id": service_id,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "address": address,
            "status": status,
            "created_at": datetime.utcnow()
        }