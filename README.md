# Elder Care MVP

一個用於長者照護的位置追蹤系統，提供即時位置更新和資料庫管理功能。

## 🚀 功能特色

- **即時位置更新**: 每秒更新使用者位置座標
- **平滑移動軌跡**: 模擬真實的室內移動行為
- **RESTful API**: 提供完整的位置資料存取介面
- **資料庫管理**: 使用 PostgreSQL 和 Alembic 進行資料管理
- **Docker 支援**: 容器化部署支援

## 📋 系統需求

- Python 3.12+
- PostgreSQL 資料庫
- uv (Python 套件管理器)

## 🛠️ 安裝設置

### 1. 克隆專案

```bash
git clone <your-repository-url>
cd elder_care_mvp
```

### 2. 安裝依賴

```bash
uv sync
```

### 3. 環境變數設置

確保你的 PostgreSQL 資料庫連接字串正確設置在 `app/data/__init__.py` 中：

```python
engine = create_engine("postgresql://username:password@host:port/database")
```

## 🏃‍♂️ 運行應用程式

### 本地開發

```bash
# 啟動應用程式
uv run python -m app.main
```

### 使用 Docker

```bash
# 建置 Docker 映像
docker build -t elder-care-mvp .

# 運行容器
docker run -p 8000:8000 elder-care-mvp
```

## 📊 API 端點

### 基礎端點

- `GET /` - 應用程式狀態
- `GET /health` - 健康檢查

### 使用者位置 API

- `GET /api/v1/user/` - 獲取所有使用者位置（即時更新）
- `POST /api/v1/user/start-updates` - 啟動位置更新服務
- `POST /api/v1/user/stop-updates` - 停止位置更新服務
- `GET /api/v1/user/update-status` - 查看更新服務狀態

### 使用範例

```bash
# 獲取即時位置資料
curl http://localhost:8000/api/v1/user/

# 查看更新狀態
curl http://localhost:8000/api/v1/user/update-status

# 控制更新服務
curl -X POST http://localhost:8000/api/v1/user/stop-updates
curl -X POST http://localhost:8000/api/v1/user/start-updates
```

## 🗄️ 資料庫管理

### 初始設置

應用程式啟動時會自動創建必要的資料庫表格。

### 使用 Alembic 管理遷移

#### 檢查遷移狀態

```bash
uv run alembic current
```

#### 創建新遷移

```bash
uv run alembic revision --autogenerate -m "描述你的變更"
```

#### 應用遷移

```bash
uv run alembic upgrade head
```

#### 回滾遷移

```bash
uv run alembic downgrade -1
```

#### 查看遷移歷史

```bash
uv run alembic history
```

## 📁 專案結構

```
elder_care_mvp/
├── app/
│   ├── data/              # 資料庫操作
│   │   ├── __init__.py    # 資料庫連接
│   │   └── user_info.py   # 使用者資料操作
│   ├── fake/              # 模擬資料
│   │   ├── __init__.py
│   │   ├── location.py    # 位置資料
│   │   └── user_info.py   # 使用者資料
│   ├── model/             # 資料模型
│   │   └── user_info.py   # UserInfo 模型
│   ├── service/           # 業務邏輯
│   │   ├── location_updater.py  # 位置更新服務
│   │   └── user_info.py   # 使用者服務
│   ├── web/               # Web API
│   │   └── user_info.py   # 使用者 API 路由
│   └── main.py            # 應用程式入口
├── alembic/               # 資料庫遷移
│   ├── versions/          # 遷移檔案
│   ├── env.py             # 遷移環境配置
│   └── script.py.mako     # 遷移模板
├── alembic.ini            # Alembic 配置
├── pyproject.toml         # 專案配置
├── Dockerfile             # Docker 配置
└── README.md              # 專案說明
```

## 🔧 配置說明

### 位置範圍設定

在 `app/service/location_updater.py` 中可以調整位置範圍：

```python
self.x_range = (1.0, 66.93)      # X 座標範圍
self.z_range = (-11.84, 25.3)    # Z 座標範圍
self.y_value = 0.0               # Y 座標（固定值）
```

### 移動速度設定

```python
self._movement_speed = 0.5  # 移動速度（弧度/秒）
```

## 🚀 部署到 Render

### 1. 連接 GitHub 倉庫

在 Render 中連接你的 GitHub 倉庫。

### 2. 設置部署配置

- **Name**: `elder_care_mvp`
- **Language**: `Docker`
- **Branch**: `main`
- **Region**: 選擇適合的地區
- **Root Directory**: 保持空白（使用根目錄）

### 3. 環境變數

確保在 Render 中設置正確的資料庫連接字串。

## 🐛 故障排除

### 常見問題

1. **資料庫連接錯誤**

   - 檢查 PostgreSQL 連接字串
   - 確認資料庫服務正在運行

2. **Alembic 遷移問題**

   - 確保 `alembic.ini` 中的資料庫 URL 正確
   - 檢查 `alembic/env.py` 中的模型導入

3. **位置更新不工作**
   - 檢查 `location_updater` 服務是否正常啟動
   - 查看應用程式日誌

### 日誌檢查

```bash
# 查看應用程式日誌
uv run python -m app.main

# 檢查資料庫連接
uv run alembic current
```

## 📝 開發指南

### 添加新功能

1. 在 `app/model/` 中定義資料模型
2. 在 `app/service/` 中實現業務邏輯
3. 在 `app/web/` 中添加 API 路由
4. 使用 Alembic 創建資料庫遷移

### 代碼風格

- 使用英文註解
- 遵循 PEP 8 代碼風格
- 添加適當的類型提示

## 📄 授權

本專案僅供學習和開發使用。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

**注意**: 請確保在生產環境中設置適當的安全措施和環境變數。
