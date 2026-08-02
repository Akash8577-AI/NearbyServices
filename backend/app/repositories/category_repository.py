from bson import ObjectId

from app.db.mongodb import db


class CategoryRepository:

    collection = db.categories

    @staticmethod
    async def create(category: dict):
        result = await CategoryRepository.collection.insert_one(category)
        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        categories = []

        async for category in CategoryRepository.collection.find():
            category["id"] = str(category["_id"])
            del category["_id"]
            categories.append(category)

        return categories

    @staticmethod
    async def get_by_id(category_id: str):
        category = await CategoryRepository.collection.find_one(
            {"_id": ObjectId(category_id)}
        )

        if category:
            category["id"] = str(category["_id"])
            del category["_id"]

        return category

    @staticmethod
    async def get_by_name(name: str):
        return await CategoryRepository.collection.find_one(
            {"name": name}
        )

    @staticmethod
    async def update(category_id: str, category: dict):
        result = await CategoryRepository.collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": category}
        )

        return result.modified_count

    @staticmethod
    async def delete(category_id: str):
        result = await CategoryRepository.collection.delete_one(
            {"_id": ObjectId(category_id)}
        )

        return result.deleted_count
    