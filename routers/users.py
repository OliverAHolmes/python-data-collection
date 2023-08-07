from fastapi import APIRouter, HTTPException, status
from models import User
from schemas.user import UserRead
from crud.user import get_all_users, delete_user_by_id, create_new_user

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def get_users():
    results = get_all_users()
    if not results:
        return []
    return results


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user = delete_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user_id not found"
        )
    return


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(user: User):
    return create_new_user(user)
