#!/usr/bin/env python3
"""
詳細測試軌跡移動邏輯
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def test_trajectory_logic():
    """測試軌跡邏輯"""

    print("=== 詳細測試軌跡移動邏輯 ===\n")

    # 老闆提供的軌跡數據（前幾個點）
    expected_trajectories = {
        "user_1": [
            (64.4, -1.9),  # 第1個點
            (55.9, -1.9),  # 第2個點
            (55.9, -8.1),  # 第3個點
            (20, -8.1),    # 第4個點
            (20, 7),       # 第5個點
        ],
        "user_2": [
            (22, 21.7),    # 第1個點
            (22, 7),       # 第2個點
            (34, 7),       # 第3個點
            (34, 15.5),    # 第4個點
            (34, 7),       # 第5個點
        ],
        "user_3": [
            (42.1, 7),     # 第1個點
            (42.1, 24.3),  # 第2個點
            (42.1, 7),     # 第3個點
            (53.8, 7),     # 第4個點
            (53.8, 30.8),  # 第5個點
        ]
    }

    try:
        # 重置所有軌跡
        print("1. 重置所有軌跡...")
        response = requests.post(f"{BASE_URL}/reset-all-trajectories")
        print(f"   結果: {response.json()}")

        # 等待一秒讓重置生效
        time.sleep(1)

        # 逐步驗證每個用戶的軌跡
        for user_id in ["user_1", "user_2", "user_3"]:
            print(f"\n=== 驗證 {user_id} 軌跡 ===")
            expected_trajectory = expected_trajectories[user_id]

            for step in range(5):  # 測試前5個點
                print(f"\n  步驟 {step + 1}:")

                # 獲取當前位置
                response = requests.get(f"{BASE_URL}/")
                data = response.json()

                # 找到對應的用戶
                user = next((u for u in data['locations'] if u['userId'] == user_id), None)
                if user:
                    actual_pos = (user['x'], user['z'])
                    expected_pos = expected_trajectory[step]

                    print(f"    實際位置: x={user['x']}, z={user['z']}")
                    print(f"    期望位置: x={expected_pos[0]}, z={expected_pos[1]}")

                    if actual_pos == expected_pos:
                        print(f"    ✅ 位置正確")
                    else:
                        print(f"    ❌ 位置錯誤！")
                        print(f"    差異: x={abs(user['x'] - expected_pos[0])}, z={abs(user['z'] - expected_pos[1])}")

                # 等待一秒讓位置更新
                time.sleep(1)

        print("\n=== 測試完成 ===")

    except Exception as e:
        print(f"❌ 錯誤: {e}")

def check_initial_positions():
    """檢查初始位置"""

    print("\n=== 檢查初始位置 ===\n")

    try:
        # 重置軌跡
        requests.post(f"{BASE_URL}/reset-all-trajectories")
        time.sleep(1)

        # 獲取位置
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        print("重置後的初始位置:")
        for user in data['locations']:
            print(f"  {user['userId']}: x={user['x']}, z={user['z']}")

        # 檢查是否符合預期
        expected_initial = {
            "user_1": (64.4, -1.9),
            "user_2": (22, 21.7),
            "user_3": (42.1, 7)
        }

        print("\n驗證初始位置:")
        for user in data['locations']:
            user_id = user['userId']
            actual = (user['x'], user['z'])
            expected = expected_initial[user_id]

            if actual == expected:
                print(f"  {user_id}: ✅ 正確")
            else:
                print(f"  {user_id}: ❌ 錯誤 (實際: {actual}, 期望: {expected})")

    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    check_initial_positions()
    test_trajectory_logic()