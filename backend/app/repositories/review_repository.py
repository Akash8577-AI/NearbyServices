from bson import ObjectId

from app.db.mongodb import db


class ReviewRepository:

    collection = db.reviews

    @staticmethod
    async def create(review: dict):
        result = await ReviewRepository.collection.insert_one(
            review
        )
        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        reviews = []

        async for review in ReviewRepository.collection.find():
            review["id"] = str(review["_id"])
            del review["_id"]
            reviews.append(review)

        return reviews

    @staticmethod
    async def get_by_id(review_id: str):
        review = await ReviewRepository.collection.find_one(
            {
                "_id": ObjectId(review_id)
            }
        )

        if review:
            review["id"] = str(review["_id"])
            del review["_id"]

        return review

    @staticmethod
    async def get_by_booking(booking_id: str):
        return await ReviewRepository.collection.find_one(
            {
                "booking_id": booking_id
            }
        )

    @staticmethod
    async def get_by_provider(provider_id: str):
        reviews = []

        async for review in ReviewRepository.collection.find(
            {
                "provider_id": provider_id
            }
        ):
            review["id"] = str(review["_id"])
            del review["_id"]
            reviews.append(review)

        return reviews

    @staticmethod
    async def update(review_id: str, review: dict):
        result = await ReviewRepository.collection.update_one(
            {
                "_id": ObjectId(review_id)
            },
            {
                "$set": review
            }
        )

        return result.modified_count

    @staticmethod
    async def delete(review_id: str):
        result = await ReviewRepository.collection.delete_one(
            {
                "_id": ObjectId(review_id)
            }
        )

        return result.deleted_count

    @staticmethod
    async def get_provider_rating(provider_id: str):
        pipeline = [
            {
                "$match": {
                    "provider_id": provider_id
                }
            },
            {
                "$group": {
                    "_id": "$provider_id",
                    "average_rating": {
                        "$avg": "$rating"
                    },
                    "total_reviews": {
                        "$sum": 1
                    }
                }
            }
        ]

        result = await ReviewRepository.collection.aggregate(
            pipeline
        ).to_list(1)

        if result:
            return {
                "average_rating": round(
                    result[0]["average_rating"],
                    2
                ),
                "total_reviews": result[0]["total_reviews"]
            }

        return {
            "average_rating": 0,
            "total_reviews": 0
        }