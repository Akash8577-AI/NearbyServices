from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    booking_id: str
    rating: int = Field(ge=1, le=5)
    review: str


class ReviewUpdate(BaseModel):
    rating: int = Field(ge=1, le=5)
    review: str