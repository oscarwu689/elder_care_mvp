from sqlalchemy import text

from app.model.user_info import UserInfo
from . import engine


def get_user_info():
    """Get all user info from database"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user_info ORDER BY timestamp DESC"))
        return result.fetchall()

def insert_user_info(user_info: UserInfo):
    """Insert new user info record using UserInfo object"""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO user_info (user_id, timestamp, x, y, z, floor, device_name, sensor_status)
            VALUES (:user_id, :timestamp, :x, :y, :z, :floor, :device_name, :sensor_status)
        """), {
            "user_id": user_info.userId,
            "timestamp": user_info.timestamp,
            "x": user_info.x,
            "y": user_info.y,
            "z": user_info.z,
            "floor": user_info.floor,
            "device_name": user_info.deviceName,
            "sensor_status": user_info.sensorStatus
        })
        conn.commit()

def get_user_info_by_id(user_id: str):
    """Get user info by user id"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user_info WHERE user_id = :user_id"), {"user_id": user_id})
        return result.fetchone()

def delete_user_info_by_id(user_id: str):
    """Delete user info by user id"""
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM user_info WHERE user_id = :user_id"), {"user_id": user_id})
        conn.commit()