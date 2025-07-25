
from app.data.user_info import delete_user_info_by_id, get_user_info, get_user_info_by_id, insert_user_info
from app.model.user_info import UserInfo


def get_user_info_from_db():
    """Get user information from database"""
    return get_user_info()

def insert_user_info_to_db(user_info: UserInfo):
    """Insert user information to database"""
    insert_user_info(user_info)

def get_user_info_by_id_from_db(user_id: str):
    """Get user information by user id from database"""
    return get_user_info_by_id(user_id)

def delete_user_info_by_id_from_db(user_id: str):
    """Delete user information by user id from database"""
    delete_user_info_by_id(user_id)