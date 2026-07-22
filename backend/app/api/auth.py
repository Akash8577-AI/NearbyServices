from fastapi import APIRouter, HTTPException

from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import AuthService
from fastapi import Depends
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: UserRegister):

    try:
        return await AuthService.register(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin):
    return await AuthService.login(user)


@router.get("/me")
async def get_profile(current_user=Depends(get_current_user)):
    return current_user