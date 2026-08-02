from datetime import datetime
from typing import Optional


class Category:

    @staticmethod
    def create(
        name: str,
        description: Optional[str] = None
    ):
        return {
            "name": name,
            "description": description,
            "created_at": datetime.utcnow()
        }