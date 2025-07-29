#!/usr/bin/env python3
"""
簡單測試軌跡邏輯
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def simple_test():
    """簡單測試"""

    print("=== 簡單軌跡測試 ===\n")

    try:
        # 重置軌跡
        print("1. 重置軌跡...")
        requests.post(f"{BASE_URL}/reset-all-trajectories")
        time.sleep(1)

        # 檢查初始位置
        print("\n2. 檢查初始位置...")
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        for user in data['locations']:
            print(f"  {user['userId']}: x={user['x']}, z={user['z']}")

        # 等待幾秒，觀察位置變化
        print("\n3. 觀察位置變化 (5秒)...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n  時間 {i+1}s:")
            for user in data['locations']:
                print(f"    {user['userId']}: x={user['x']}, z={user['z']}")

            time.sleep(1)

        print("\n=== 測試完成 ===")

        # 檢查是否符合預期
        print("\n預期軌跡順序:")
        print("user_1: (64.4,-1.9) → (55.9,-1.9) → (55.9,-8.1) → (20,-8.1) → (20,7)")
        print("user_2: (22,21.7) → (22,7) → (34,7) → (34,15.5) → (34,7)")
        print("user_3: (42.1,7) → (42.1,24.3) → (42.1,7) → (53.8,7) → (53.8,30.8)")

    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    simple_test()