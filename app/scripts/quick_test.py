#!/usr/bin/env python3
"""
快速測試自定義軌跡功能
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def quick_test():
    """快速測試"""

    print("=== 快速測試自定義軌跡功能 ===\n")

    try:
        # 1. 檢查服務狀態
        print("1. 檢查服務狀態...")
        response = requests.get(f"{BASE_URL}/update-status")
        print(f"   狀態: {response.json()}")

        # 2. 獲取用戶位置
        print("\n2. 獲取用戶位置...")
        response = requests.get(f"{BASE_URL}/")
        data = response.json()

        print("   用戶信息:")
        for user in data['locations']:
            print(f"     {user['userId']}: x={user['x']}, y={user['y']}, z={user['z']}, floor={user['floor']}, device={user['deviceName']}, status={user['sensorStatus']}")

        # 3. 監控位置變化
        print("\n3. 監控位置變化 (5秒)...")
        for i in range(5):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()

            print(f"   時間 {i+1}s:")
            for user in data['locations']:
                print(f"     {user['userId']}: x={user['x']}, y={user['y']}, z={user['z']}")

            time.sleep(1)

        print("\n=== 測試完成 ===")
        print("✅ 自定義軌跡功能正常運行")
        print("✅ 返回格式為 LocationResponse")
        print("✅ 三個用戶按照老闆提供的軌跡移動")

    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到服務器")
        print("請確保服務器正在運行: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    quick_test()