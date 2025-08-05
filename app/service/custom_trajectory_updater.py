import asyncio
import time
import math
from typing import List, Dict, Tuple
from app.model.user_info import UserInfo

class CustomTrajectoryUpdater:
    def __init__(self):
        self._users: List[UserInfo] = []
        self._running = False
        self._task = None
        self._time_offset = 0.0

        # 老闆提供的原始軌跡數據
        self._original_trajectories = {
            "2024": [
                (64.4, -1.9), (55.9, -1.9), (55.9, -8.1), (20, -8.1),
                (20, 7), (9.5, 7), (9.5, 17.5), (9.5, 7),
                (22, 7), (22, 21.7), (22, 7), (34, 7),
                (34, 15.5), (34, 7), (42.1, 7), (42.1, 24.3),
                (42.1, 7), (53.8, 7), (53.8, 30.8), (63.5, 30.8),
                (63.5, 15.2), (54.1, 15.2), (54.1, 8.4), (64.4, -1.9)
            ],
            "2026": [
                (22, 21.7), (22, 7), (34, 7), (34, 15.5),
                (34, 7), (42.1, 7), (42.1, 24.3), (42.1, 7),
                (53.8, 7), (53.8, 30.8), (63.5, 30.8), (63.5, 15.2),
                (54.1, 15.2), (54.1, 8.4), (64.4, -1.9), (55.9, -1.9),
                (55.9, -8.1), (20, -8.1), (20, 7), (9.5, 7),
                (9.5, 17.5), (9.5, 7), (22, 7), (22, 21.7)
            ],
            "92": [
                (42.1, 7), (42.1, 24.3), (42.1, 7), (53.8, 7),
                (53.8, 30.8), (63.5, 30.8), (63.5, 15.2), (54.1, 15.2),
                (54.1, 8.4), (64.4, -1.9), (55.9, -1.9), (55.9, -8.1),
                (20, -8.1), (20, 7), (9.5, 7), (9.5, 17.5),
                (9.5, 7), (22, 7), (22, 21.7), (22, 7),
                (34, 7), (34, 15.5), (34, 7), (42.1, 7)
            ],
            "2353": [
                (17.3, -16.2), (25.0, -10.0), (35.0, -5.0), (45.0, 0.0),
                (55.0, 5.0), (65.0, 10.0), (55.0, 15.0), (45.0, 20.0),
                (35.0, 15.0), (25.0, 10.0), (15.0, 5.0), (5.0, 0.0),
                (15.0, -5.0), (25.0, -10.0), (35.0, -15.0), (45.0, -20.0),
                (35.0, -15.0), (25.0, -10.0), (15.0, -5.0), (5.0, 0.0),
                (15.0, 5.0), (25.0, 10.0), (35.0, 15.0), (17.3, -16.2)
            ]
        }

        # 內插後的軌跡數據
        self._trajectories = {}
        self._interpolation_points = 10  # 每兩個點之間插入的點數

        # 生成內插軌跡
        self._generate_interpolated_trajectories()

        # each user's trajectory index
        self._trajectory_indices = {}
        self._y_value = 0.0

    def _interpolate_between_points(self, point1: Tuple[float, float], point2: Tuple[float, float], num_points: int) -> List[Tuple[float, float]]:
        """在兩個點之間進行線性內插"""
        x1, z1 = point1
        x2, z2 = point2

        interpolated_points = []
        for i in range(num_points + 1):  # +1 包含起始點
            t = i / num_points  # 插值參數 (0 到 1)
            x = x1 + (x2 - x1) * t
            z = z1 + (z2 - z1) * t
            interpolated_points.append((round(x, 2), round(z, 2)))

        return interpolated_points

    def _generate_interpolated_trajectories(self):
        """生成內插後的軌跡數據"""
        for user_id, original_trajectory in self._original_trajectories.items():
            interpolated_trajectory = []

            for i in range(len(original_trajectory)):
                current_point = original_trajectory[i]
                next_point = original_trajectory[(i + 1) % len(original_trajectory)]  # 循環到第一個點

                # 在當前點和下一個點之間進行內插
                interpolated_segment = self._interpolate_between_points(
                    current_point,
                    next_point,
                    self._interpolation_points
                )

                # 添加內插點（除了最後一個點，避免重複）
                if i < len(original_trajectory) - 1:
                    interpolated_trajectory.extend(interpolated_segment[:-1])  # 不包含最後一個點
                else:
                    # 最後一段包含所有點，確保軌跡閉合
                    interpolated_trajectory.extend(interpolated_segment)

            self._trajectories[user_id] = interpolated_trajectory

    def set_interpolation_points(self, num_points: int):
        """設置內插點數"""
        self._interpolation_points = num_points
        self._generate_interpolated_trajectories()
        # 重置所有用戶的軌跡索引
        for user_id in self._trajectory_indices:
            self._trajectory_indices[user_id] = 0

    def get_interpolation_info(self) -> Dict:
        """獲取內插信息"""
        info = {}
        for user_id in self._original_trajectories:
            original_count = len(self._original_trajectories[user_id])
            interpolated_count = len(self._trajectories[user_id])
            info[user_id] = {
                "original_points": original_count,
                "interpolated_points": interpolated_count,
                "interpolation_points_per_segment": self._interpolation_points,
                "total_segments": original_count
            }
        return info

    def start(self):
        """Start the custom trajectory update loop"""
        if not self._running:
            self._running = True
            self._time_offset = time.time()
            self._task = asyncio.create_task(self._update_loop())
            print("Custom trajectory update service started")

    def stop(self):
        """Stop the custom trajectory update loop"""
        self._running = False
        if self._task:
            self._task.cancel()
            print("Custom trajectory update service stopped")

    def set_users(self, users: List[UserInfo]):
        """Set the list of users to update"""
        self._users = users.copy()
        # initialize trajectory index
        for user in self._users:
            if user.userId in self._trajectories:
                self._trajectory_indices[user.userId] = 0
            else:
                # if user has no defined trajectory, use default trajectory
                self._trajectory_indices[user.userId] = 0

    def get_users(self) -> List[UserInfo]:
        """Get the current list of users"""
        return self._users.copy()

    def _get_next_position(self, user_id: str) -> Tuple[float, float]:
        """Get the next trajectory point position"""
        if user_id not in self._trajectories:
            # if user has no defined trajectory, return current position
            return None, None

        trajectory = self._trajectories[user_id]
        current_index = self._trajectory_indices.get(user_id, 0)

        # get current trajectory point
        x, z = trajectory[current_index]

        # update index to the next point (loop)
        next_index = (current_index + 1) % len(trajectory)
        self._trajectory_indices[user_id] = next_index

        return x, z

    async def _update_loop(self):
        """Main loop for updating positions every second"""
        while self._running:
            try:
                # Update each user's position
                for user in self._users:
                    # get next trajectory point
                    new_x, new_z = self._get_next_position(user.userId)

                    if new_x is not None and new_z is not None:
                        # Update user position
                        user.x = new_x
                        user.y = self._y_value
                        user.z = new_z
                        user.timestamp = int(time.time() * 1000)  # Update timestamp

                # Wait N second
                await asyncio.sleep(2)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Custom trajectory update error: {e}")
                await asyncio.sleep(1)

    def get_trajectory_info(self) -> Dict:
        """Get trajectory information"""
        info = {}
        for user_id, trajectory in self._trajectories.items():
            info[user_id] = {
                "total_points": len(trajectory),
                "current_index": self._trajectory_indices.get(user_id, 0),
                "trajectory": trajectory
            }
        return info

    def reset_trajectory(self, user_id: str = None):
        """Reset trajectory index"""
        if user_id:
            if user_id in self._trajectory_indices:
                self._trajectory_indices[user_id] = 0
        else:
            # reset all users
            for user_id in self._trajectory_indices:
                self._trajectory_indices[user_id] = 0

# Global instance
custom_trajectory_updater = CustomTrajectoryUpdater()