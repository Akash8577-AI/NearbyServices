from datetime import datetime
from bson.errors import InvalidId
from fastapi import HTTPException
from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from app.repositories.provider_repository import ProviderRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate
)

class BookingService:

    @staticmethod
    async def create(
        booking: BookingCreate,
        customer_id: str
    ):
        service = await ServiceRepository.get_by_id(
            booking.service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        provider = await ProviderRepository.get_by_id(
            booking.provider_id
        )

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        if provider["service_id"] != booking.service_id:
            raise HTTPException(
                status_code=400,
                detail="Provider does not belong to selected service"
            )

        if not provider["is_available"]:
            raise HTTPException(
                status_code=400,
                detail="Provider is currently unavailable"
            )

        try:
            booking_date = datetime.strptime(
                booking.booking_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking date format. Use YYYY-MM-DD"
            )

        if booking_date < datetime.today().date():
            raise HTTPException(
                status_code=400,
                detail="Booking date cannot be in the past"
            )

        try:
            datetime.strptime(
                booking.booking_time,
                "%H:%M"
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking time format. Use HH:MM"
            )

        if not booking.address.strip():
            raise HTTPException(
                status_code=400,
                detail="Address is required"
            )

        existing_booking = await BookingRepository.find_duplicate_booking(
            customer_id=customer_id,
            provider_id=booking.provider_id,
            booking_date=booking.booking_date,
            booking_time=booking.booking_time
        )

        if existing_booking:
            raise HTTPException(
                status_code=409,
                detail="You already have a booking for this provider at the selected date and time"
            )

        new_booking = Booking.create(
            customer_id=customer_id,
            provider_id=booking.provider_id,
            service_id=booking.service_id,
            booking_date=booking.booking_date,
            booking_time=booking.booking_time,
            address=booking.address
        )
        booking_id = await BookingRepository.create(new_booking)

        return {
            "id": booking_id,
            "customer_id": customer_id,
            "provider_id": booking.provider_id,
            "service_id": booking.service_id,
            "booking_date": booking.booking_date,
            "booking_time": booking.booking_time,
            "address": booking.address
        }

    @staticmethod
    async def get_all():
        return await BookingRepository.get_all()

    @staticmethod
    async def get_by_id(booking_id: str):
        try:
            booking = await BookingRepository.get_by_id(
                booking_id
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

        return booking

    @staticmethod
    async def update(
        booking_id: str,
        booking: BookingUpdate,
        customer_id: str
    ):
        try:
            existing_booking = await BookingRepository.get_by_id(
                booking_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking id"
            )

        if not existing_booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if existing_booking["customer_id"] != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update this booking"
            )

        if existing_booking["status"] == "Completed":
            raise HTTPException(
                status_code=400,
                detail="Completed booking cannot be updated"
            )

        if existing_booking["status"] == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cancelled booking cannot be updated"
            )

        try:
            booking_date = datetime.strptime(
                booking.booking_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking date format. Use YYYY-MM-DD"
            )

        if booking_date < datetime.today().date():
            raise HTTPException(
                status_code=400,
                detail="Booking date cannot be in the past"
            )

        try:
            datetime.strptime(
                booking.booking_time,
                "%H:%M"
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking time format. Use HH:MM"
            )

        if not booking.address.strip():
            raise HTTPException(
                status_code=400,
                detail="Address is required"
            )

        duplicate = await BookingRepository.find_duplicate_booking(
            customer_id=customer_id,
            provider_id=existing_booking["provider_id"],
            booking_date=booking.booking_date,
            booking_time=booking.booking_time,
            exclude_booking_id=booking_id
        )

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="You already have another booking at the selected date and time"
            )

        update_data = {
            "booking_date": booking.booking_date,
            "booking_time": booking.booking_time,
            "address": booking.address
        }

        updated = await BookingRepository.update(
            booking_id,
            update_data
        )

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Booking could not be updated"
            )

        return {
            "message": "Booking updated successfully"
        }

    @staticmethod
    async def cancel(
        booking_id: str,
        customer_id: str
    ):
        try:
            booking = await BookingRepository.get_by_id(
                booking_id
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
                detail="You are not allowed to cancel this booking"
            )

        if booking["status"] == "Completed":
            raise HTTPException(
                status_code=400,
                detail="Completed booking cannot be cancelled"
            )

        if booking["status"] == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Booking is already cancelled"
            )

        updated = await BookingRepository.update(
            booking_id,
            {"status": "Cancelled"}
        )

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Booking could not be cancelled"
            )

        return {
            "message": "Booking cancelled successfully"
        }

    @staticmethod
    async def update_status(
        booking_id: str,
        status: str
    ):
        try:
            booking = await BookingRepository.get_by_id(
                booking_id
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

        allowed_status = [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ]

        if status not in allowed_status:
            raise HTTPException(
                status_code=400,
                detail="Invalid booking status"
            )

        if booking["status"] == "Completed":
            raise HTTPException(
                status_code=400,
                detail="Completed booking cannot be updated"
            )

        if booking["status"] == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cancelled booking cannot be updated"
            )

        updated = await BookingRepository.update(
            booking_id,
            {"status": status}
        )

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Status update failed"
            )

        return {
            "message": "Booking status updated successfully"
        }

    @staticmethod
    async def get_my_bookings(customer_id: str):
        return await BookingRepository.get_by_customer(
            customer_id
        )

    @staticmethod
    async def get_provider_bookings(provider_id: str):
        return await BookingRepository.get_by_provider(
            provider_id
        )

