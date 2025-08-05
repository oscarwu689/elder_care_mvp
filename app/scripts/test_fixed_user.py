#!/usr/bin/env python3
"""
測試用戶 2353 固定位置
驗證用戶 2353 的位置是否保持不變
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def test_fixed_user_2353():
    """測試用戶 2353 固定位置"""

    print("=== 測試用戶 2353 固定位置 ===\n")

    try:
        # 1. 重置軌跡
        print("1. 重置軌跡...")
        response = requests.post(f"{BASE_URL}/reset-all-trajectories")
        print(f"   結果: {response.json()}")
        time.sleep(1)

        # 2. 獲取初始位置
        print("\n2. 獲取初始位置...")
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        user_2353_initial = next((u for u in data['locations'] if u['userId'] == '2353'), None)
        if user_2353_initial:
            print(f"   用戶 2353 初始位置: x={user_2353_initial['x']}, z={user_2353_initial['z']}")

        # 3. 啟動自定義軌跡
        print("\n3. 啟動自定義軌跡...")
        response = requests.post(f"{BASE_URL}/start-custom-trajectory")
        print(f"   結果: {response.json()}")

        # 4. 監控所有用戶位置變化
        print("\n4. 監控位置變化 (10秒)...")
        user_2353_positions = []

        for i in range(10):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n   時間 {i+1}:")
            for user in data['locations']:
                if user['userId'] == '2353':
                    user_2353_positions.append((user['x'], user['z']))
                    print(f"     {user['userId']}: x={user['x']}, z={user['z']} (固定)")
                else:
                    print(f"     {user['userId']}: x={user['x']}, z={user['z']} (移動)")

            time.sleep(1)

        # 5. 停止服務
        print("\n5. 停止服務...")
        response = requests.post(f"{BASE_URL}/stop-custom-trajectory")
        print(f"   結果: {response.json()}")

        # 6. 分析結果
        print("\n6. 分析結果...")
        if user_2353_positions:
            initial_pos = user_2353_positions[0]
            all_same = all(pos == initial_pos for pos in user_2353_positions)

            if all_same:
                print(f"   ✅ 用戶 2353 位置保持固定: x={initial_pos[0]}, z={initial_pos[1]}")
            else:
                print(f"   ❌ 用戶 2353 位置有變化")
                print(f"   初始位置: {initial_pos}")
                print(f"   最終位置: {user_2353_positions[-1]}")

        print("\n=== 測試完成 ===")

    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到服務器")
        print("請確保服務器正在運行: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def compare_mobile_vs_fixed_users():
    """比較移動用戶和固定用戶"""

    print("\n=== 比較移動用戶和固定用戶 ===\n")

    try:
        # 重置並啟動
        requests.post(f"{BASE_URL}/reset-all-trajectories")
        requests.post(f"{BASE_URL}/start-custom-trajectory")
        time.sleep(1)

        # 記錄初始位置
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        initial_positions = {}
        for user in data['locations']:
            initial_positions[user['userId']] = (user['x'], user['z'])

        print("初始位置:")
        for user_id, pos in initial_positions.items():
            print(f"  {user_id}: x={pos[0]}, z={pos[1]}")

        # 監控5秒
        print("\n監控5秒...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n時間 {i+1}:")
            for user in data['locations']:
                current_pos = (user['x'], user['z'])
                initial_pos = initial_positions[user['userId']]

                if current_pos == initial_pos:
                    status = "固定"
                else:
                    status = "移動"

                print(f"  {user['userId']}: x={user['x']}, z={user['z']} ({status})")

            time.sleep(1)

        # 停止服務
        requests.post(f"{BASE_URL}/stop-custom-trajectory")

        print("\n=== 比較完成 ===")
        print("✅ 用戶 2024, 2026, 92 應該移動")
        print("✅ 用戶 2353 應該保持固定")

    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_fixed_user_2353()
    compare_mobile_vs_fixed_users()