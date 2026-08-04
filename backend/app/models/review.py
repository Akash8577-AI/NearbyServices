from datetime import datetime


class Review:

    @staticmethod
    def create(
        booking_id: str,
        customer_id: str,
        provider_id: str,
        rating: int,
        review: str
    ):
        return {
            "booking_id": booking_id,
            "customer_id": customer_id,
            "provider_id": provider_id,
            "rating": rating,
            "review": review,
            "created_at": datetime.utcnow()
        }