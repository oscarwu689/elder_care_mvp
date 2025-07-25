from fastapi import APIRouter
from app.service.user_info import get_all_users, start_location_updates, stop_location_updates, get_update_status

router = APIRouter(prefix="/api/v1/user")


@router.get("/")
def get_users():
    return get_all_users()


@router.post("/start-updates")
def start_updates():
    """啟動位置更新服務"""
    return start_location_updates()


@router.post("/stop-updates")
def stop_updates():
    """停止位置更新服務"""
    return stop_location_updates()


@router.get("/update-status")
def get_status():
    """獲取更新服務狀態"""
    return get_update_status()