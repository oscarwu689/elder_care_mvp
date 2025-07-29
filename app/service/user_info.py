from app.data.user_info import get_user_info, insert_user_info
from app.fake.location import _location_data
from app.model.user_info import UserInfo, LocationResponse
from app.service.location_updater import location_updater
from app.service.custom_trajectory_updater import custom_trajectory_updater

def get_all_users():
    """Get all user information (including real-time location updates)"""
    # If custom trajectory updater is running, return real-time data
    if custom_trajectory_updater._running:
        users = custom_trajectory_updater.get_users()
        return LocationResponse(locations=users)
    # If location updater is running, return real-time data
    elif location_updater._running:
        users = location_updater.get_users()
        return LocationResponse(locations=users)
    else:
        # Otherwise return static data
        return LocationResponse(locations=_location_data)

def start_location_updates():
    """Start location update service"""
    if not location_updater._running:
        # Set initial user data
        location_updater.set_users(_location_data)
        # Start update loop
        location_updater.start()
    return {"message": "Location update service started"}

def start_custom_trajectory_updates():
    """Start custom trajectory update service"""
    if not custom_trajectory_updater._running:
        # Set initial user data
        custom_trajectory_updater.set_users(_location_data)
        # Start update loop
        custom_trajectory_updater.start()
    return {"message": "Custom trajectory update service started"}

def stop_location_updates():
    """Stop location update service"""
    location_updater.stop()
    return {"message": "Location update service stopped"}

def stop_custom_trajectory_updates():
    """Stop custom trajectory update service"""
    custom_trajectory_updater.stop()
    return {"message": "Custom trajectory update service stopped"}

def get_update_status():
    """Get update service status"""
    return {
        "location_updater_running": location_updater._running,
        "custom_trajectory_running": custom_trajectory_updater._running,
        "user_count": len(location_updater.get_users()) if location_updater._running else len(custom_trajectory_updater.get_users()) if custom_trajectory_updater._running else len(_location_data)
    }

def get_trajectory_info():
    """Get custom trajectory information"""
    return custom_trajectory_updater.get_trajectory_info()

def reset_trajectory(user_id: str = None):
    """Reset trajectory indices"""
    custom_trajectory_updater.reset_trajectory(user_id)
    return {"message": f"Trajectory reset for {user_id if user_id else 'all users'}"}
