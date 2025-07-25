from app.data.user_info import get_user_info, insert_user_info
from app.fake.location import _location_data
from app.model.user_info import UserInfo
from app.service.location_updater import location_updater

def get_all_users():
    """Get all user information (including real-time location updates)"""
    # If location updater is running, return real-time data
    if location_updater._running:
        return location_updater.get_users()
    else:
        # Otherwise return static data
        return _location_data

def start_location_updates():
    """Start location update service"""
    if not location_updater._running:
        # Set initial user data
        location_updater.set_users(_location_data)
        # Start update loop
        location_updater.start()
    return {"message": "Location update service started"}

def stop_location_updates():
    """Stop location update service"""
    location_updater.stop()
    return {"message": "Location update service stopped"}

def get_update_status():
    """Get update service status"""
    return {
        "running": location_updater._running,
        "user_count": len(location_updater.get_users())
    }
