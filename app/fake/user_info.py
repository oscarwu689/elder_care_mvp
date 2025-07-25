from app.model.user_info import UserInfo


_user_info_1 = UserInfo(
    userId="user_1",
    timestamp=1716729600,
    x=50,
    y=0,
    z=0,
    floor=1,
    deviceName="device1",
    sensorStatus="normal"
)

_user_info_2 = UserInfo(
    userId="user_2",
    timestamp=1716729600,
    x=0,
    y=0,
    z=10,
    floor=1,
    deviceName="device2",
    sensorStatus="low_battery"
)