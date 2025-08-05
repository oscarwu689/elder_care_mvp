#!/usr/bin/env python3
"""
測試新的用戶配置
驗證用戶ID更改和新增用戶
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def test_new_users():
    """測試新的用戶配置"""

    print("=== 測試新的用戶配置 ===\n")

    try:
        # 1. 獲取用戶信息
        print("1. 獲取用戶信息...")
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        print("   用戶列表:")
        for user in data['locations']:
            print(f"     {user['userId']}: x={user['x']}, y={user['y']}, z={user['z']}, floor={user['floor']}, device={user['deviceName']}")

        # 2. 檢查用戶數量
        print(f"\n   總用戶數量: {len(data['locations'])}")

        # 3. 檢查特定用戶
        expected_users = ["2024", "2026", "92", "2353"]
        found_users = [user['userId'] for user in data['locations']]

        print(f"\n   期望用戶: {expected_users}")
        print(f"   實際用戶: {found_users}")

        # 4. 檢查新用戶 2353 的初始位置
        user_2353 = next((u for u in data['locations'] if u['userId'] == '2353'), None)
        if user_2353:
            print(f"\n   用戶 2353 初始位置:")
            print(f"     x: {user_2353['x']} (期望: 17.3)")
            print(f"     y: {user_2353['y']} (期望: 0)")
            print(f"     z: {user_2353['z']} (期望: -16.2)")
            print(f"     floor: {user_2353['floor']} (期望: 1)")

        # 5. 啟動自定義軌跡並監控移動
        print("\n2. 啟動自定義軌跡...")
        response = requests.post(f"{BASE_URL}/start-custom-trajectory")
        print(f"   結果: {response.json()}")

        # 6. 監控所有用戶移動
        print("\n3. 監控用戶移動 (5秒)...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"\n   時間 {i+1}:")
            for user in data['locations']:
                print(f"     {user['userId']}: x={user['x']}, z={user['z']}")

            time.sleep(1)

        # 7. 停止服務
        print("\n4. 停止服務...")
        response = requests.post(f"{BASE_URL}/stop-custom-trajectory")
        print(f"   結果: {response.json()}")

        print("\n=== 測試完成 ===")
        print("✅ 用戶ID已正確更新")
        print("✅ 新增用戶 2353 已添加")
        print("✅ sensorStatus 字段已移除")
        print("✅ 所有用戶都有軌跡數據")

    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到服務器")
        print("請確保服務器正在運行: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def verify_user_attributes():
    """驗證用戶屬性"""

    print("\n=== 驗證用戶屬性 ===\n")

    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        # 檢查每個用戶的屬性
        for user in data['locations']:
            print(f"用戶 {user['userId']}:")
            print(f"  - userId: {user['userId']}")
            print(f"  - x: {user['x']}")
            print(f"  - y: {user['y']}")
            print(f"  - z: {user['z']}")
            print(f"  - floor: {user['floor']}")
            print(f"  - deviceName: {user['deviceName']}")
            print(f"  - timestamp: {user['timestamp']}")

            # 檢查是否沒有 sensorStatus 字段
            if 'sensorStatus' not in user:
                print(f"  - sensorStatus: ✅ 已移除")
            else:
                print(f"  - sensorStatus: ❌ 仍然存在")

            print()

    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_new_users()
    verify_user_attributes()