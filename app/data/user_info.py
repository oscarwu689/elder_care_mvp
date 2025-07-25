from sqlalchemy import text

from app.model.user_info import UserInfo
from . import engine


def get_user_info():
    """Get all user info from database"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user_info ORDER BY timestamp DESC"))
        rows = result.fetchall()

        # Convert Row objects to UserInfo models
        user_list = []
        for row in rows:
            user_info = UserInfo(
                userId=row[1],
                timestamp=row[2],
                x=float(row[3]),
                y=float(row[4]),
                z=float(row[5]),
                floor=row[6],
                deviceName=row[7],
                sensorStatus=row[8]
            )
            user_list.append(user_info)

        return user_list

def insert_user_info(user_info: UserInfo):
    """Insert new user info record using UserInfo object"""
    with engine.connect() as conn:
        # Prepare the data, excluding timestamp if it's None (will use database default)
        data = {
            "user_id": user_info.userId,
            "x": user_info.x,
            "y": user_info.y,
            "z": user_info.z,
            "floor": user_info.floor,
            "device_name": user_info.deviceName,
            "sensor_status": user_info.sensorStatus
        }

        if user_info.timestamp is not None:
            # If timestamp is provided, include it in the insert
            conn.execute(text("""
                INSERT INTO user_info (user_id, timestamp, x, y, z, floor, device_name, sensor_status)
                VALUES (:user_id, :timestamp, :x, :y, :z, :floor, :device_name, :sensor_status)
            """), {**data, "timestamp": user_info.timestamp})
        else:
            # If timestamp is not provided, let database use the default
            conn.execute(text("""
                INSERT INTO user_info (user_id, x, y, z, floor, device_name, sensor_status)
                VALUES (:user_id, :x, :y, :z, :floor, :device_name, :sensor_status)
            """), data)

        conn.commit()

def get_user_info_by_id(user_id: str):
    """Get user info by user id"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM user_info WHERE user_id = :user_id"), {"user_id": user_id})
        row = result.fetchone()

        if row:
            user_info = UserInfo(
                userId=row[1],
                timestamp=row[2],
                x=float(row[3]),
                y=float(row[4]),
                z=float(row[5]),
                floor=row[6],
                deviceName=row[7],
                sensorStatus=row[8]
            )
            return user_info.model_dump()
        return None

def delete_user_info_by_id(user_id: str):
    """Delete user info by user id"""
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM user_info WHERE user_id = :user_id"), {"user_id": user_id})
        conn.commit()