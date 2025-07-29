import asyncio
import time
from typing import List, Dict, Tuple
from app.model.user_info import UserInfo

class CustomTrajectoryUpdater:
    def __init__(self):
        self._users: List[UserInfo] = []
        self._running = False
        self._task = None
        self._time_offset = 0.0

        # fake data
        self._trajectories = {
            "user_1": [
                (64.4, -1.9), (55.9, -1.9), (55.9, -8.1), (20, -8.1),
                (20, 7), (9.5, 7), (9.5, 17.5), (9.5, 7),
                (22, 7), (22, 21.7), (22, 7), (34, 7),
                (34, 15.5), (34, 7), (42.1, 7), (42.1, 24.3),
                (42.1, 7), (53.8, 7), (53.8, 30.8), (63.5, 30.8),
                (63.5, 15.2), (54.1, 15.2), (54.1, 8.4), (64.4, -1.9)
            ],
            "user_2": [
                (22, 21.7), (22, 7), (34, 7), (34, 15.5),
                (34, 7), (42.1, 7), (42.1, 24.3), (42.1, 7),
                (53.8, 7), (53.8, 30.8), (63.5, 30.8), (63.5, 15.2),
                (54.1, 15.2), (54.1, 8.4), (64.4, -1.9), (55.9, -1.9),
                (55.9, -8.1), (20, -8.1), (20, 7), (9.5, 7),
                (9.5, 17.5), (9.5, 7), (22, 7), (22, 21.7)
            ],
            "user_3": [
                (42.1, 7), (42.1, 24.3), (42.1, 7), (53.8, 7),
                (53.8, 30.8), (63.5, 30.8), (63.5, 15.2), (54.1, 15.2),
                (54.1, 8.4), (64.4, -1.9), (55.9, -1.9), (55.9, -8.1),
                (20, -8.1), (20, 7), (9.5, 7), (9.5, 17.5),
                (9.5, 7), (22, 7), (22, 21.7), (22, 7),
                (34, 7), (34, 15.5), (34, 7), (42.1, 7)
            ]
        }

        # each user's trajectory index
        self._trajectory_indices = {}
        self._y_value = 0.0

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