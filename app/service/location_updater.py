import asyncio
import random
import time
from typing import List
from app.model.user_info import UserInfo

class LocationUpdater:
    def __init__(self):
        self._users: List[UserInfo] = []
        self._running = False
        self._task = None
        
        # 位置範圍設定
        self.x_range = (1.0, 66.93)
        self.z_range = (-11.84, 25.3)
        self.y_value = 0.0
        
    def start(self):
        """啟動位置更新循環"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._update_loop())
            print("位置更新服務已啟動")
    
    def stop(self):
        """停止位置更新循環"""
        self._running = False
        if self._task:
            self._task.cancel()
            print("位置更新服務已停止")
    
    def set_users(self, users: List[UserInfo]):
        """設定要更新的使用者列表"""
        self._users = users.copy()
    
    def get_users(self) -> List[UserInfo]:
        """獲取當前使用者列表"""
        return self._users.copy()
    
    async def _update_loop(self):
        """每秒更新位置的主循環"""
        while self._running:
            try:
                # 更新每個使用者的位置
                for user in self._users:
                    # 生成新的 X 和 Z 值
                    new_x = random.uniform(self.x_range[0], self.x_range[1])
                    new_z = random.uniform(self.z_range[0], self.z_range[1])
                    
                    # 更新使用者位置
                    user.x = round(new_x, 2)
                    user.y = self.y_value
                    user.z = round(new_z, 2)
                    user.timestamp = int(time.time() * 1000)  # 更新時間戳
                
                # 等待 1 秒
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"位置更新錯誤: {e}")
                await asyncio.sleep(1)

# 全域實例
location_updater = LocationUpdater() 