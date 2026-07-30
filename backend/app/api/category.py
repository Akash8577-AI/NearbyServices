from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.models.role import UserRole
from app.schemas.category import CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/")
async def create_category(
    category: CategoryCreate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return await CategoryService.create(category)


@router.get("/")
async def get_categories():
    return await CategoryService.get_all()


@router.get("/{category_id}")
async def get_category(category_id: str):
    return await CategoryService.get_by_id(category_id)