from fastapi import APIRouter, HTTPException

from app.schemas.user import UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: UserRegister):

    try:
        return await AuthService.register(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))