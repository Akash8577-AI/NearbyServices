from bson.errors import InvalidId
from fastapi import HTTPException
from app.repositories.provider_repository import ProviderRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.booking_repository import BookingRepository
from app.models.review import Review
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate
)

class ReviewService:

    @staticmethod
    async def create(
        review: ReviewCreate,
        customer_id: str
    ):
        try:
            booking = await BookingRepository.get_by_id(
                review.booking_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking id"
            )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking["customer_id"] != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can review only your own booking"
            )

        if booking["status"] != "Completed":
            raise HTTPException(
                status_code=400,
                detail="Only completed bookings can be reviewed"
            )

        existing_review = await ReviewRepository.get_by_booking(
            review.booking_id
        )

        if existing_review:
            raise HTTPException(
                status_code=409,
                detail="Review already submitted for this booking"
            )

        new_review = Review.create(
            booking_id=review.booking_id,
            customer_id=customer_id,
            provider_id=booking["provider_id"],
            rating=review.rating,
            review=review.review
        )

        review_id = await ReviewRepository.create(
            new_review
        )

        rating = await ReviewRepository.get_provider_rating(
            booking["provider_id"]
        )

        await ProviderRepository.update_rating(
            booking["provider_id"],
            rating["average_rating"],
            rating["total_reviews"]
        )

        return {
            "id": review_id,
            "message": "Review submitted successfully"
        }

    @staticmethod
    async def update(
        review_id: str,
        review: ReviewUpdate,
        customer_id: str
    ):
        try:
            existing_review = await ReviewRepository.get_by_id(
                review_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid review id"
            )

        if not existing_review:
            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        if existing_review["customer_id"] != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can update only your own review"
            )

        update_data = {
            "rating": review.rating,
            "review": review.review
        }

        updated = await ReviewRepository.update(
            review_id,
            update_data
        )

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Review could not be updated"
            )

        rating = await ReviewRepository.get_provider_rating(
            existing_review["provider_id"]
        )

        await ProviderRepository.update_rating(
            existing_review["provider_id"],
            rating["average_rating"],
            rating["total_reviews"]
        )

        return {
            "message": "Review updated successfully"
        }

    @staticmethod
    async def get_all():
        return await ReviewRepository.get_all()

    @staticmethod
    async def get_by_id(review_id: str):
        try:
            review = await ReviewRepository.get_by_id(
                review_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid review id"
            )

        if not review:
            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        return review

    @staticmethod
    async def get_provider_reviews(
        provider_id: str
    ):
        return await ReviewRepository.get_by_provider(
            provider_id
        )

    @staticmethod
    async def delete(
        review_id: str,
        customer_id: str
    ):
        try:
            existing_review = await ReviewRepository.get_by_id(
                review_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid review id"
            )

        if not existing_review:
            raise HTTPException(
                status_code=404,
                detail="Review not found"
            )

        if existing_review["customer_id"] != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can delete only your own review"
            )

        deleted = await ReviewRepository.delete(
            review_id
        )

        if not deleted:
            raise HTTPException(
                status_code=400,
                detail="Review could not be deleted"
            )

        rating = await ReviewRepository.get_provider_rating(
            existing_review["provider_id"]
        )

        await ProviderRepository.update_rating(
            existing_review["provider_id"],
            rating["average_rating"],
            rating["total_reviews"]
        )

        return {
            "message": "Review deleted successfully"
        }