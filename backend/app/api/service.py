from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.models.role import UserRole
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate
)
from app.services.service_service import ServiceService

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.post("/")
async def create_service(
    service: ServiceCreate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ServiceService.create(service)


@router.get("/")
async def get_services():
    return await ServiceService.get_all()


@router.get("/{service_id}")
async def get_service(service_id: str):
    return await ServiceService.get_by_id(service_id)


@router.put("/{service_id}")
async def update_service(
    service_id: str,
    service: ServiceUpdate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ServiceService.update(
        service_id,
        service
    )


@router.delete("/{service_id}")
async def delete_service(
    service_id: str,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ServiceService.delete(service_id)

