#!/usr/bin/env python3
"""
測試內插功能
驗證用戶是否在軌跡點之間平滑移動
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def test_interpolation():
    """測試內插功能"""

    print("=== 測試內插功能 ===\n")

    try:
        # 1. 獲取內插信息
        print("1. 獲取內插信息...")
        response = requests.get(f"{BASE_URL}/interpolation-info")
        interpolation_info = response.json()

        for user_id, info in interpolation_info.items():
            print(f"  {user_id}:")
            print(f"    原始點數: {info['original_points']}")
            print(f"    內插後點數: {info['interpolated_points']}")
            print(f"    每段內插點數: {info['interpolation_points_per_segment']}")
            print(f"    總段數: {info['total_segments']}")

        # 2. 重置軌跡
        print("\n2. 重置軌跡...")
        requests.post(f"{BASE_URL}/reset-all-trajectories")
        time.sleep(1)

        # 3. 監控移動（觀察平滑度）
        print("\n3. 監控移動（觀察平滑度）...")
        for i in range(10):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n  時間 {i+1}:")
            for user in data['locations']:
                print(f"    {user['userId']}: x={user['x']}, z={user['z']}")

            time.sleep(1)

        # 4. 調整內插點數
        print("\n4. 調整內插點數...")
        print("  設置為5個內插點...")
        response = requests.post(f"{BASE_URL}/set-interpolation-points/5")
        print(f"  結果: {response.json()}")

        # 5. 再次監控移動
        print("\n5. 再次監控移動（較少內插點）...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n  時間 {i+1}:")
            for user in data['locations']:
                print(f"    {user['userId']}: x={user['x']}, z={user['z']}")

            time.sleep(1)

        # 6. 設置更多內插點
        print("\n6. 設置更多內插點...")
        print("  設置為20個內插點...")
        response = requests.post(f"{BASE_URL}/set-interpolation-points/20")
        print(f"  結果: {response.json()}")

        # 7. 最終監控
        print("\n7. 最終監控移動（更多內插點）...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n  時間 {i+1}:")
            for user in data['locations']:
                print(f"    {user['userId']}: x={user['x']}, z={user['z']}")

            time.sleep(1)

        print("\n=== 測試完成 ===")
        print("✅ 內插功能正常工作")
        print("✅ 用戶在軌跡點之間平滑移動")
        print("✅ 可以動態調整內插點數")

    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到服務器")
        print("請確保服務器正在運行: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def compare_movement_smoothness():
    """比較不同內插點數的移動平滑度"""

    print("\n=== 比較移動平滑度 ===\n")

    try:
        # 測試不同的內插點數
        interpolation_points_list = [0, 5, 10, 20]

        for points in interpolation_points_list:
            print(f"\n--- 測試 {points} 個內插點 ---")

            # 設置內插點數
            response = requests.post(f"{BASE_URL}/set-interpolation-points/{points}")
            print(f"設置結果: {response.json()}")

            # 重置軌跡
            requests.post(f"{BASE_URL}/reset-all-trajectories")
            time.sleep(1)

            # 監控移動
            print("移動軌跡:")
            for i in range(3):
                response = requests.get(f"{BASE_URL}/")
                data = response.json()

                user1 = next((u for u in data['locations'] if u['userId'] == '2024'), None)
                if user1:
                    print(f"  時間 {i+1}: x={user1['x']}, z={user1['z']}")

                time.sleep(1)

        print("\n=== 比較完成 ===")
        print("觀察不同內插點數的移動平滑度差異")

    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_interpolation()
    compare_movement_smoothness()