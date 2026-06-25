from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.deps import CurrentUserDep, DbDep
from app.core.security import create_access_token
from app.schemas.user import UserRead
from app.services.user import UserService

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbDep,
) -> TokenResponse:
    user = await UserService(db).authenticate(form.username, form.password)
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)
