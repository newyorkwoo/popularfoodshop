# Popular Food Shop 美食電商平台

> 類 IFCHIC 風格食品電商網站 — Vue 3 + FastAPI + PostgreSQL

## 技術架構

### Frontend

- **Vue 3** + **Vite** — SPA 前端
- **Pinia** — 狀態管理
- **Vue Router** — 路由
- **Tailwind CSS 4** — 樣式框架
- **vue-i18n** — 中英雙語
- **Axios** — HTTP 請求

### Backend

- **FastAPI** — Python 非同步 API 框架
- **SQLAlchemy 2** (async) — ORM
- **PostgreSQL 16** — 主資料庫
- **Redis 7** — 快取 / 會話
- **Alembic** — 資料庫遷移
- **python-jose / passlib** — JWT + 密碼雜湊

---

## 快速開始

### 1. 啟動資料庫 (Docker)

```bash
docker-compose up -d db redis
```

### 2. Backend 設定

```bash
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
pip install -r requirements.txt
cp .env.example .env            # 編輯設定
```

### 3. 資料庫遷移 & 種子資料

```bash
cd backend
alembic upgrade head
python -m app.seeds.seed
```

### 4. 啟動 Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 5. Frontend 設定

```bash
cd frontend
npm install
npm run dev
```

### 6. 開啟瀏覽器

- 前端: http://localhost:5173
- API 文件: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## 預設帳號

| 角色   | Email                      | 密碼          |
| ------ | -------------------------- | ------------- |
| 管理員 | admin@popularfoodshop.com  | Admin@123456  |
| 編輯   | editor@popularfoodshop.com | Editor@123456 |
| 會員   | user@example.com           | User@123456   |

---

## 專案結構

```
popularfoodshop/
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── assets/           # 靜態資源
│   │   ├── components/       # 元件
│   │   ├── layouts/          # 版面配置
│   │   ├── pages/            # 頁面
│   │   ├── router/           # 路由
│   │   ├── services/         # API 服務
│   │   ├── stores/           # Pinia 狀態
│   │   └── i18n/             # 多語言
│   └── package.json
├── backend/                   # FastAPI 後端
│   ├── app/
│   │   ├── models/           # SQLAlchemy 模型
│   │   ├── schemas/          # Pydantic 結構
│   │   ├── routers/          # API 路由
│   │   │   └── admin/        # 管理後台 API
│   │   ├── middleware/       # 中間件
│   │   ├── utils/            # 工具
│   │   ├── seeds/            # 種子資料
│   │   ├── config.py         # 環境設定
│   │   ├── database.py       # DB 連線
│   │   ├── dependencies.py   # FastAPI 依賴
│   │   └── main.py           # App 入口
│   ├── alembic/              # 資料庫遷移
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── skills.md                  # 完整規格書
└── README.md
```

---

## API 端點總覽

### 認證 `/api/v1/auth`

- `POST /register` — 註冊
- `POST /login` — 登入
- `POST /refresh` — 更新 Token
- `POST /logout` — 登出
- `POST /forgot-password` — 忘記密碼
- `POST /reset-password` — 重設密碼
- `GET /me` — 取得個人資料

### 會員 `/api/v1/users`

- `PUT /profile` — 更新資料
- `PUT /password` — 修改密碼
- `CRUD /addresses` — 收件地址
- `CRUD /cards` — 信用卡

### 商品 `/api/v1/products`

- `GET /` — 商品列表
- `GET /search` — 搜尋
- `GET /trending` — 熱門
- `GET /:id` — 詳情
- `GET /:id/reviews` — 評價
- `POST /:id/reviews` — 新增評價

### 分類 & 品牌

- `GET /categories` — 分類樹
- `GET /categories/:slug/products`
- `GET /brands` — 品牌列表
- `GET /brands/:slug/products`

### 購物車 `/api/v1/cart`

- `GET /` — 取得購物車
- `POST /items` — 加入
- `PUT /items/:id` — 更新數量
- `DELETE /items/:id` — 移除
- `POST /coupon` — 套用優惠券

### 訂單 `/api/v1/orders`

- `POST /` — 建立訂單
- `GET /` — 訂單列表
- `GET /:id` — 訂單詳情
- `POST /:id/cancel` — 取消
- `POST /:id/return` — 退貨

### 管理後台 `/api/v1/admin/*`

- Dashboard / Products / Orders / Users / Promotions / Content / Reports / Settings

---

## License

Private — 僅供學習用途
