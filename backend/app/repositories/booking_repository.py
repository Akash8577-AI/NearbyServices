from bson import ObjectId

from app.db.mongodb import db


class BookingRepository:

    collection = db.bookings

    @staticmethod
    async def create(booking: dict):
        result = await BookingRepository.collection.insert_one(
            booking
        )
        return str(result.inserted_id)

    @staticmethod
    async def get_all():
        bookings = []

        async for booking in BookingRepository.collection.find():
            booking["id"] = str(booking["_id"])
            del booking["_id"]
            bookings.append(booking)

        return bookings

    @staticmethod
    async def get_by_id(booking_id: str):
        booking = await BookingRepository.collection.find_one(
            {"_id": ObjectId(booking_id)}
        )

        if booking:
            booking["id"] = str(booking["_id"])
            del booking["_id"]

        return booking

    @staticmethod
    async def update(booking_id: str, booking: dict):
        result = await BookingRepository.collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": booking}
        )

        return result.modified_count

    @staticmethod
    async def delete(booking_id: str):
        result = await BookingRepository.collection.delete_one(
            {"_id": ObjectId(booking_id)}
        )

        return result.deleted_count

    @staticmethod
    async def get_by_customer(customer_id: str):
        bookings = []

        async for booking in BookingRepository.collection.find(
            {"customer_id": customer_id}
        ):
            booking["id"] = str(booking["_id"])
            del booking["_id"]
            bookings.append(booking)

        return bookings

    @staticmethod
    async def get_by_provider(provider_id: str):
        bookings = []

        async for booking in BookingRepository.collection.find(
            {"provider_id": provider_id}
        ):
            booking["id"] = str(booking["_id"])
            del booking["_id"]
            bookings.append(booking)

        return bookings

    @staticmethod
    async def find_duplicate_booking(
        customer_id: str,
        provider_id: str,
        booking_date: str,
        booking_time: str,
        exclude_booking_id: str = None
    ):
        query = {
            "customer_id": customer_id,
            "provider_id": provider_id,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "status": {"$ne": "Cancelled"}
        }

        if exclude_booking_id:
            query["_id"] = {"$ne": ObjectId(exclude_booking_id)}

        return await BookingRepository.collection.find_one(query)