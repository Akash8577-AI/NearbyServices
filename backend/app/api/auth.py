from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_current_user
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
    )




@router.post("/register")
async def register(user: UserRegister):

    try:
        return await AuthService.register(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return await AuthService.login(user)


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user)
):
    current_user["_id"] = str(current_user["_id"])
    return {
    "id": current_user["_id"],
    "full_name": current_user["full_name"],
    "email": current_user["email"],
    "phone": current_user["phone"],
    "role": current_user["role"],
    "created_at": current_user["created_at"]
}