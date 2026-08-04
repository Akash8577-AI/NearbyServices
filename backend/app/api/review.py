from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate
)
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/")
async def create_review(
    review: ReviewCreate,
    current_user=Depends(get_current_user)
):
    return await ReviewService.create(
        review,
        str(current_user["_id"])
    )


@router.get("/")
async def get_all_reviews():
    return await ReviewService.get_all()


@router.get("/{review_id}")
async def get_review(
    review_id: str
):
    return await ReviewService.get_by_id(
        review_id
    )


@router.get("/provider/{provider_id}")
async def get_provider_reviews(
    provider_id: str
):
    return await ReviewService.get_provider_reviews(
        provider_id
    )


@router.put("/{review_id}")
async def update_review(
    review_id: str,
    review: ReviewUpdate,
    current_user=Depends(get_current_user)
):
    return await ReviewService.update(
        review_id,
        review,
        str(current_user["_id"])
    )


@router.delete("/{review_id}")
async def delete_review(
    review_id: str,
    current_user=Depends(get_current_user)
):
    return await ReviewService.delete(
        review_id,
        str(current_user["_id"])
    )