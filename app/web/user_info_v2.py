from fastapi import APIRouter

from app.model.user_info import UserInfo
from app.service.user_info_db import delete_user_info_by_id_from_db, get_user_info_by_id_from_db, get_user_info_from_db, insert_user_info_to_db

router = APIRouter(prefix="/api/v2/user")

@router.get("")
def get_users():
    return get_user_info_from_db()

@router.post("/")
def insert_user_info(user_info: UserInfo):
    return insert_user_info_to_db(user_info)

@router.get("/{user_id}")
def get_user_info_by_id(user_id: str):
    return get_user_info_by_id_from_db(user_id)

@router.delete("/{user_id}")
def delete_user_info_by_id(user_id: str):
    return delete_user_info_by_id_from_db(user_id)