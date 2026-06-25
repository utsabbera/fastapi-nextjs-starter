from fastapi import APIRouter, status

from app.core.deps import CurrentUserDep, DbDep
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: DbDep) -> UserRead:
    user = await UserService(db).register(data)
    return UserRead.model_validate(user)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user: CurrentUserDep, db: DbDep) -> None:
    await UserRepository(db).delete(current_user)
