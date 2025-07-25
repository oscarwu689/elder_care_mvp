from fastapi import APIRouter
from app.service.user_info import get_all_users

router = APIRouter(prefix="/api/v1/user")


@router.get("/")
def get_users():
    return get_all_users()