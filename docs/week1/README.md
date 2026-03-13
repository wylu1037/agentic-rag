# 第 1 周交付物（工程骨架）

## 交付清单

1. Backend：`backend/`（FastAPI + pytest + ruff）
2. Frontend：`frontend/`（Next.js App Router + TypeScript）
3. Infra：`infra/docker-compose.yml`（Postgres+pgvector + Redis）

## 本地启动顺序

```bash
docker compose -f infra/docker-compose.yml up -d
```

```bash
cd backend
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

## Definition of Done（第 1 周）

1. `GET /health` 可用。
2. Next.js 首页可访问。
3. Postgres 与 Redis 容器均健康。
