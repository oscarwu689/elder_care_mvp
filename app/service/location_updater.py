import asyncio
import math
import time
from typing import List
from app.model.user_info import UserInfo

class LocationUpdater:
    def __init__(self):
        self._users: List[UserInfo] = []
        self._running = False
        self._task = None

        # Position range settings
        self.x_range = (1.0, 66.93)
        self.z_range = (-11.84, 25.3)
        self.y_value = 0.0

        # Movement trajectory parameters
        self._time_offset = 0.0
        self._movement_speed = 0.5  # Movement speed (radians/second)

    def start(self):
        """Start the position update loop"""
        if not self._running:
            self._running = True
            self._time_offset = time.time()
            self._task = asyncio.create_task(self._update_loop())
            print("Location update service started")

    def stop(self):
        """Stop the position update loop"""
        self._running = False
        if self._task:
            self._task.cancel()
            print("Location update service stopped")

    def set_users(self, users: List[UserInfo]):
        """Set the list of users to update"""
        self._users = users.copy()

    def get_users(self) -> List[UserInfo]:
        """Get the current list of users"""
        return self._users.copy()

    def _calculate_position(self, user_index: int, current_time: float) -> tuple[float, float]:
        """Calculate user position on the trajectory"""
        # Set different starting angles for each user so they move along different trajectories
        base_angle = current_time * self._movement_speed + (user_index * math.pi / 2)

        # Use elliptical trajectory for more natural movement
        center_x = (self.x_range[0] + self.x_range[1]) / 2
        center_z = (self.z_range[0] + self.z_range[1]) / 2

        # Ellipse radius
        radius_x = (self.x_range[1] - self.x_range[0]) / 3
        radius_z = (self.z_range[1] - self.z_range[0]) / 3

        # Calculate position on elliptical trajectory
        x = center_x + radius_x * math.cos(base_angle)
        z = center_z + radius_z * math.sin(base_angle * 1.5)  # Slightly different frequency for more complex trajectory

        # Ensure within range
        x = max(self.x_range[0], min(self.x_range[1], x))
        z = max(self.z_range[0], min(self.z_range[1], z))

        return round(x, 2), round(z, 2)

    async def _update_loop(self):
        """Main loop for updating positions every second"""
        while self._running:
            try:
                current_time = time.time() - self._time_offset

                # Update each user's position
                for i, user in enumerate(self._users):
                    # Calculate new position
                    new_x, new_z = self._calculate_position(i, current_time)

                    # Update user position
                    user.x = new_x
                    user.y = self.y_value
                    user.z = new_z
                    user.timestamp = int(time.time() * 1000)  # Update timestamp

                # Wait 1 second
                await asyncio.sleep(1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Position update error: {e}")
                await asyncio.sleep(1)

# Global instance
location_updater = LocationUpdater()