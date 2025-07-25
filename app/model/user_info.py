from typing import List
from pydantic import BaseModel

class UserInfo(BaseModel):
    userId: str
    timestamp: int  # Unix timestamp in milliseconds
    x: float
    y: float
    z: float
    floor: int
    deviceName: str
    sensorStatus: str

class LocationResponse(BaseModel):
    locations: List[UserInfo]