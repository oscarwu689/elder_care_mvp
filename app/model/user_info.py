from typing import List, Optional
from pydantic import BaseModel

class UserInfo(BaseModel):
    userId: str
    timestamp: Optional[int] = None  # Unix timestamp in milliseconds (optional, will use default if not provided)
    x: float
    y: float
    z: float
    floor: int
    deviceName: str

class LocationResponse(BaseModel):
    locations: List[UserInfo]