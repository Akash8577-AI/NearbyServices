from fastapi import HTTPException

from app.models.provider import Provider
from app.repositories.provider_repository import ProviderRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.provider import (
    ProviderCreate,
    ProviderUpdate
)


class ProviderService:

    @staticmethod
    async def create(provider: ProviderCreate):

        # Check if service exists
        service = await ServiceRepository.get_by_id(
            provider.service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        existing_email = await ProviderRepository.get_by_email(
            provider.email
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Provider with this email already exists"
            )

        existing_phone = await ProviderRepository.get_by_phone(
            provider.phone
        )

        if existing_phone:
            raise HTTPException(
                status_code=400,
                detail="Provider with this phone already exists"
            )

        new_provider = Provider.create(
            service_id=provider.service_id,
            full_name=provider.full_name,
            phone=provider.phone,
            email=provider.email,
            experience=provider.experience,
            address=provider.address,
            is_available=provider.is_available
        )

        provider_id = await ProviderRepository.create(
            new_provider
        )

        return {
            "message": "Provider created successfully",
            "provider_id": provider_id
        }

    @staticmethod
    async def get_all():
        return await ProviderRepository.get_all()

    @staticmethod
    async def get_by_id(provider_id: str):

        provider = await ProviderRepository.get_by_id(
            provider_id
        )

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        return provider

    @staticmethod
    async def update(
        provider_id: str,
        provider: ProviderUpdate
    ):

        existing_provider = await ProviderRepository.get_by_id(
            provider_id
        )

        if not existing_provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        service = await ServiceRepository.get_by_id(
            provider.service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        duplicate_email = await ProviderRepository.get_by_email(
            provider.email
        )

        if (
            duplicate_email
            and str(duplicate_email["_id"]) != provider_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Provider with this email already exists"
            )

        duplicate_phone = await ProviderRepository.get_by_phone(
            provider.phone
        )

        if (
            duplicate_phone
            and str(duplicate_phone["_id"]) != provider_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Provider with this phone already exists"
            )

        updated_provider = {
            "service_id": provider.service_id,
            "full_name": provider.full_name,
            "phone": provider.phone,
            "email": provider.email,
            "experience": provider.experience,
            "address": provider.address,
            "is_available": provider.is_available
        }

        await ProviderRepository.update(
            provider_id,
            updated_provider
        )

        return {
            "message": "Provider updated successfully"
        }

    @staticmethod
    async def delete(provider_id: str):

        existing_provider = await ProviderRepository.get_by_id(
            provider_id
        )

        if not existing_provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        await ProviderRepository.delete(provider_id)

        return {
            "message": "Provider deleted successfully"
        }

    @staticmethod
    async def get_by_service(service_id: str):
        return await ProviderRepository.get_by_service(
            service_id
        )