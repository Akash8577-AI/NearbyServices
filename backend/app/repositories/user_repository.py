from app.db.mongodb import db


class UserRepository:

    @staticmethod
    async def get_by_email(email: str):
        return await db.users.find_one(
            {"email": email})

    @staticmethod
    async def create(user: dict):
        result = await db.users.insert_one(user)
        return str(result.inserted_id)