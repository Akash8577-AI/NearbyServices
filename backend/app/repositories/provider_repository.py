from bson import ObjectId

from app.db.mongodb import db


class ProviderRepository:

    collection = db.providers

    @staticmethod
    async def create(provider: dict):
        result = await ProviderRepository.collection.insert_one(provider)
        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        providers = []

        async for provider in ProviderRepository.collection.find():
            provider["id"] = str(provider["_id"])
            del provider["_id"]
            providers.append(provider)

        return providers

    @staticmethod
    async def get_by_id(provider_id: str):
        provider = await ProviderRepository.collection.find_one(
            {"_id": ObjectId(provider_id)}
        )

        if provider:
            provider["id"] = str(provider["_id"])
            del provider["_id"]

        return provider

    @staticmethod
    async def update(provider_id: str, provider: dict):
        result = await ProviderRepository.collection.update_one(
            {"_id": ObjectId(provider_id)},
            {"$set": provider}
        )

        return result.modified_count

    @staticmethod
    async def delete(provider_id: str):
        result = await ProviderRepository.collection.delete_one(
            {"_id": ObjectId(provider_id)}
        )

        return result.deleted_count

    @staticmethod
    async def get_by_service(service_id: str):
        providers = []

        async for provider in ProviderRepository.collection.find(
            {"service_id": service_id}
        ):
            provider["id"] = str(provider["_id"])
            del provider["_id"]
            providers.append(provider)

        return providers

    @staticmethod
    async def get_by_email(email: str):
        provider = await ProviderRepository.collection.find_one(
            {"email": email}
        )

        if provider:
            provider["id"] = str(provider["_id"])
            del provider["_id"]

        return provider

    @staticmethod
    async def get_by_phone(phone: str):
        provider = await ProviderRepository.collection.find_one(
            {"phone": phone}
        )

        if provider:
            provider["id"] = str(provider["_id"])
            del provider["_id"]

        return provider