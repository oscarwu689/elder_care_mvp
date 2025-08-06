#!/usr/bin/env python3
"""
測試固定用戶
驗證用戶 92 和 2353 都保持固定位置
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1/user"

def test_fixed_users():
    """測試固定用戶"""
    
    print("=== 測試固定用戶 ===\n")
    
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
        
        print("   初始位置:")
        for user in data['locations']:
            print(f"     {user['userId']}: x={user['x']}, z={user['z']}")
        
        # 3. 啟動自定義軌跡
        print("\n3. 啟動自定義軌跡...")
        response = requests.post(f"{BASE_URL}/start-custom-trajectory")
        print(f"   結果: {response.json()}")
        
        # 4. 監控位置變化
        print("\n4. 監控位置變化 (8秒)...")
        fixed_users_positions = {"92": [], "2353": []}
        mobile_users_positions = {"2024": [], "2026": []}
        
        for i in range(8):
            response = requests.get(f"{BASE_URL}/")
            data = response.json()
            
            print(f"\n   時間 {i+1}:")
            for user in data['locations']:
                if user['userId'] in ["92", "2353"]:
                    fixed_users_positions[user['userId']].append((user['x'], user['z']))
                    print(f"     {user['userId']}: x={user['x']}, z={user['z']} (固定)")
                else:
                    mobile_users_positions[user['userId']].append((user['x'], user['z']))
                    print(f"     {user['userId']}: x={user['x']}, z={user['z']} (移動)")
            
            time.sleep(1)
        
        # 5. 停止服務
        print("\n5. 停止服務...")
        response = requests.post(f"{BASE_URL}/stop-custom-trajectory")
        print(f"   結果: {response.json()}")
        
        # 6. 分析結果
        print("\n6. 分析結果...")
        
        # 檢查固定用戶
        print("   固定用戶分析:")
        for user_id in ["92", "2353"]:
            if fixed_users_positions[user_id]:
                initial_pos = fixed_users_positions[user_id][0]
                all_same = all(pos == initial_pos for pos in fixed_users_positions[user_id])
                
                if all_same:
                    print(f"     ✅ 用戶 {user_id} 位置保持固定: x={initial_pos[0]}, z={initial_pos[1]}")
                else:
                    print(f"     ❌ 用戶 {user_id} 位置有變化")
        
        # 檢查移動用戶
        print("\n   移動用戶分析:")
        for user_id in ["2024", "2026"]:
            if mobile_users_positions[user_id]:
                initial_pos = mobile_users_positions[user_id][0]
                final_pos = mobile_users_positions[user_id][-1]
                
                if initial_pos != final_pos:
                    print(f"     ✅ 用戶 {user_id} 位置有移動: {initial_pos} → {final_pos}")
                else:
                    print(f"     ❌ 用戶 {user_id} 位置沒有移動")
        
        print("\n=== 測試完成 ===")
        
    except requests.exceptions.ConnectionError:
        print("❌ 錯誤: 無法連接到服務器")
        print("請確保服務器正在運行: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def verify_expected_positions():
    """驗證期望的位置"""
    
    print("\n=== 驗證期望位置 ===\n")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        
        expected_positions = {
            "2024": "移動中",
            "2026": "移動中", 
            "92": (6.5, 0.6),
            "2353": (17.3, -16.2)
        }
        
        print("位置驗證:")
        for user in data['locations']:
            user_id = user['userId']
            current_pos = (user['x'], user['z'])
            
            if user_id in ["92", "2353"]:
                expected = expected_positions[user_id]
                if current_pos == expected:
                    print(f"  ✅ 用戶 {user_id}: x={user['x']}, z={user['z']} (正確)")
                else:
                    print(f"  ❌ 用戶 {user_id}: x={user['x']}, z={user['z']} (期望: {expected})")
            else:
                print(f"  📍 用戶 {user_id}: x={user['x']}, z={user['z']} (移動中)")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_fixed_users()
    verify_expected_positions() 