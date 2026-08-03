from pydantic import BaseModel, EmailStr


class ProviderCreate(BaseModel):
    service_id: str
    full_name: str
    phone: str
    email: EmailStr
    experience: int
    address: str
    is_available: bool = True


class ProviderUpdate(BaseModel):
    service_id: str
    full_name: str
    phone: str
    email: EmailStr
    experience: int
    address: str
    is_available: bool


class ProviderResponse(BaseModel):
    id: str
    service_id: str
    full_name: str
    phone: str
    email: EmailStr
    experience: int
    address: str
    is_available: bool