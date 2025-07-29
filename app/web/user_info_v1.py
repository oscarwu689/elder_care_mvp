from fastapi import APIRouter
from app.service.user_info import (
    get_all_users,
    start_location_updates,
    stop_location_updates,
    get_update_status,
    start_custom_trajectory_updates,
    stop_custom_trajectory_updates,
    get_trajectory_info,
    reset_trajectory
)

router = APIRouter(prefix="/api/v1/user")


@router.get("/")
def get_users():
    return get_all_users()


@router.post("/start-updates")
def start_updates():
    """Start location update service"""
    return start_location_updates()


@router.post("/stop-updates")
def stop_updates():
    """Stop location update service"""
    return stop_location_updates()


@router.get("/update-status")
def get_status():
    """Get update service status"""
    return get_update_status()

@router.post("/start-custom-trajectory")
def start_custom_trajectory():
    """Start custom trajectory update service"""
    return start_custom_trajectory_updates()

@router.post("/stop-custom-trajectory")
def stop_custom_trajectory():
    """Stop custom trajectory update service"""
    return stop_custom_trajectory_updates()

@router.get("/trajectory-info")
def get_trajectory_info_endpoint():
    """Get custom trajectory information"""
    return get_trajectory_info()

@router.post("/reset-trajectory/{user_id}")
def reset_trajectory_endpoint(user_id: str):
    """Reset trajectory for specific user"""
    return reset_trajectory(user_id)

@router.post("/reset-all-trajectories")
def reset_all_trajectories():
    """Reset all trajectories"""
    return reset_trajectory()