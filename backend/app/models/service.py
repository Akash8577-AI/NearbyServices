from datetime import datetime


class Service:

    @staticmethod
    def create(
        category_id: str,
        name: str,
        description: str,
        price: float
    ):
        return {
            "category_id": category_id,
            "name": name,
            "description": description,
            "price": price,
            "created_at": datetime.utcnow()
        }