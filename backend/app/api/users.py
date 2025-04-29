from fastapi import APIRouter

router = APIRouter()


@router.get("/users/{user_id}", tags=["users"])
async def read_user(user_id: int):
    return {"user_id": user_id, "username": "Sample User"}


@router.post("/users/", tags=["users"])
async def create_user(user: dict):
    return {"message": "User created", "user": user}
