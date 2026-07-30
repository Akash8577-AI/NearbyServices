from datetime import datetime


class Category:

    @staticmethod
    def create(
        name: str,
        description: str
    ):
        return {
            "name": name,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }