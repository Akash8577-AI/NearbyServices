from pydantic import BaseModel


class BookingCreate(BaseModel):
    provider_id: str
    service_id: str
    booking_date: str
    booking_time: str
    address: str


class BookingUpdate(BaseModel):
    booking_date: str
    booking_time: str
    address: str


class BookingStatusUpdate(BaseModel):
    status: str


class BookingResponse(BaseModel):
    id: str
    customer_id: str
    provider_id: str
    service_id: str
    booking_date: str
    booking_time: str
    address: str
    status: str