from pydantic import BaseModel


class ServiceCreate(BaseModel):
    category_id: str
    name: str
    description: str
    price: float


class ServiceUpdate(BaseModel):
    category_id: str
    name: str
    description: str
    price: float


class ServiceResponse(BaseModel):
    id: str
    category_id: str
    name: str
    description: str
    price: float