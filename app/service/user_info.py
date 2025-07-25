from app.fake.location import _location_data
from app.service.location_updater import location_updater

def get_all_users():
    """獲取所有使用者資訊（包含即時位置更新）"""
    # 如果位置更新器正在運行，返回即時資料
    if location_updater._running:
        return location_updater.get_users()
    else:
        # 否則返回靜態資料
        return _location_data

def start_location_updates():
    """啟動位置更新服務"""
    if not location_updater._running:
        # 設定初始使用者資料
        location_updater.set_users(_location_data)
        # 啟動更新循環
        location_updater.start()
    return {"message": "位置更新服務已啟動"}

def stop_location_updates():
    """停止位置更新服務"""
    location_updater.stop()
    return {"message": "位置更新服務已停止"}

def get_update_status():
    """獲取更新服務狀態"""
    return {
        "running": location_updater._running,
        "user_count": len(location_updater.get_users())
    }