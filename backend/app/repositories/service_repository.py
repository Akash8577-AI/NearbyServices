from bson import ObjectId

from app.db.mongodb import db


class ServiceRepository:

    collection = db.services

    @staticmethod
    async def create(service: dict):
        result = await ServiceRepository.collection.insert_one(
            service
        )

        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        services = []

        async for service in ServiceRepository.collection.find():

            service["id"] = str(service["_id"])
            del service["_id"]

            services.append(service)

        return services

    @staticmethod
    async def get_by_id(service_id: str):

        service = await ServiceRepository.collection.find_one(
            {"_id": ObjectId(service_id)}
        )

        if service:
            service["id"] = str(service["_id"])
            del service["_id"]

        return service

    @staticmethod
    async def get_by_name(name: str):

        return await ServiceRepository.collection.find_one(
            {"name": name}
        )

    @staticmethod
    async def update(
        service_id: str,
        service: dict
    ):

        result = await ServiceRepository.collection.update_one(
            {"_id": ObjectId(service_id)},
            {"$set": service}
        )

        return result.modified_count

    @staticmethod
    async def delete(service_id: str):

        result = await ServiceRepository.collection.delete_one(
            {"_id": ObjectId(service_id)}
        )

        return result.deleted_count