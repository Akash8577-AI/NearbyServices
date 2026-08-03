from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.models.role import UserRole
from app.schemas.provider import (
    ProviderCreate,
    ProviderUpdate
)
from app.services.provider_service import ProviderService

router = APIRouter(
    prefix="/providers",
    tags=["Providers"]
)


@router.post("/")
async def create_provider(
    provider: ProviderCreate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ProviderService.create(provider)


@router.get("/")
async def get_providers():
    return await ProviderService.get_all()


@router.get("/{provider_id}")
async def get_provider(provider_id: str):
    return await ProviderService.get_by_id(provider_id)


@router.put("/{provider_id}")
async def update_provider(
    provider_id: str,
    provider: ProviderUpdate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ProviderService.update(
        provider_id,
        provider
    )


@router.delete("/{provider_id}")
async def delete_provider(
    provider_id: str,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await ProviderService.delete(provider_id)


@router.get("/service/{service_id}")
async def get_providers_by_service(
    service_id: str
):
    return await ProviderService.get_by_service(
        service_id
    )