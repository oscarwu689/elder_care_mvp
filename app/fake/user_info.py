from app.model.user_info import UserInfo


_user_info_1 = UserInfo(
    userId="user_1",
    timestamp=1716729600,
    x=100,
    y=100,
    z=100,
    floor=1,
    deviceName="device1",
    sensorStatus="normal"
)

_user_info_2 = UserInfo(
    userId="user_2",
    timestamp=1716729600,
    x=100,
    y=100,
    z=100,
    floor=2,
    deviceName="device2",
    sensorStatus="low_battery"
)