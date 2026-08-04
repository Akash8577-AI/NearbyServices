from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingStatusUpdate
)
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    current_user=Depends(get_current_user)
):
    return await BookingService.cancel(
        booking_id,
        str(current_user["_id"])
    )

@router.patch("/{booking_id}/status")
async def update_booking_status(
    booking_id: str,
    booking: BookingStatusUpdate
):
    return await BookingService.update_status(
        booking_id,
        booking.status
    )



@router.post("/")
async def create_booking(
    booking: BookingCreate,
    current_user=Depends(get_current_user)
):
    return await BookingService.create(
        booking,
        str(current_user["_id"])
    )


@router.get("/")
async def get_all_bookings():
    return await BookingService.get_all()


@router.get("/my")
async def get_my_bookings(
    current_user=Depends(get_current_user)
):
    return await BookingService.get_my_bookings(
        str(current_user["_id"])
    )


@router.get("/{booking_id}")
async def get_booking(
    booking_id: str
):
    return await BookingService.get_by_id(
        booking_id
    )


@router.put("/{booking_id}")
async def update_booking(
    booking_id: str,
    booking: BookingUpdate,
    current_user=Depends(get_current_user)
):
    return await BookingService.update(
        booking_id,
        booking,
        str(current_user["_id"])
    )