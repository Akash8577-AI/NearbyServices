from fastapi import HTTPException

from app.models.service import Service
from app.repositories.category_repository import CategoryRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate
)


class ServiceService:

    @staticmethod
    async def create(service: ServiceCreate):

        # Check if category exists
        category = await CategoryRepository.get_by_id(
            service.category_id
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Check duplicate service
        existing_service = await ServiceRepository.get_by_name(
            service.name
        )

        if existing_service:
            raise HTTPException(
                status_code=400,
                detail="Service already exists"
            )

        # Create service object
        new_service = Service.create(
            category_id=service.category_id,
            name=service.name,
            description=service.description,
            price=service.price
        )

        # Save service
        service_id = await ServiceRepository.create(
            new_service
        )

        return {
            "message": "Service created successfully",
            "service_id": service_id
        }

    @staticmethod
    async def get_all():
        return await ServiceRepository.get_all()

    @staticmethod
    async def get_by_id(service_id: str):

        service = await ServiceRepository.get_by_id(
            service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        return service

    @staticmethod
    async def search(name: str):
        return await ServiceRepository.search_by_name(name)

    @staticmethod
    async def update(
        service_id: str,
        service: ServiceUpdate
    ):
        # Check if service exists
        existing_service = await ServiceRepository.get_by_id(
            service_id
        )

        if not existing_service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        # Check if category exists
        category = await CategoryRepository.get_by_id(
            service.category_id
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Check duplicate service name
        duplicate = await ServiceRepository.get_by_name(
            service.name
        )

        if (
            duplicate
            and str(duplicate["_id"]) != service_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Service already exists"
            )

        updated_service = {
            "category_id": service.category_id,
            "name": service.name,
            "description": service.description,
            "price": service.price
        }

        await ServiceRepository.update(
            service_id,
            updated_service
        )

        return {
            "message": "Service updated successfully"
        }

    @staticmethod
    async def delete(service_id: str):

        existing_service = await ServiceRepository.get_by_id(
            service_id
        )

        if not existing_service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        await ServiceRepository.delete(service_id)

        return {
            "message": "Service deleted successfully"
        }
        