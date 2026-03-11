# Agentic RAG 实现路线（Python + Next.js）

本文档给出从 0 到 1 构建 Agentic RAG 的技术路线与实施步骤。

## 技术路线（3 选 1）

### 路线 A（推荐）
- 方案：`FastAPI + LangGraph + PostgreSQL/pgvector(起步) + Next.js(App Router)`
- 优点：流程可控、可测试、可解释，适合先做稳定基线再逐步 Agent 化。
- 适用：从零开始、希望兼顾上线速度与长期可维护性。

### 路线 B
- 方案：`FastAPI + LangChain 高层 Agent + Qdrant + Next.js`
- 优点：上线更快、集成成本低。
- 风险：流程可解释性与精细控制弱于 LangGraph。

### 路线 C
- 方案：`LlamaIndex Workflow + FastAPI + Next.js`
- 优点：文档连接器和检索生态强。
- 风险：复杂 Agent 编排灵活性通常不如 LangGraph。

## 推荐实施路线（7 周）

### 第 0 周：定义边界与验收标准
- 明确首批场景（如内部文档问答、客服知识助手）。
- 准备 50-100 条真实问题集与标准答案。
- 定义上线 KPI：回答正确率、引用命中率、P95 延迟、单问成本。

### 第 1 周：初始化工程骨架
- 后端：`FastAPI`、`pytest`、`ruff`、依赖管理（`uv` 或 `poetry`）。
- 前端：`Next.js App Router + TypeScript`。
- 基础设施：`docker-compose` 启动 `postgres+pgvector`、`redis`。

### 第 2 周：先完成非 Agent RAG 基线（必须）
- 文档解析与清洗（PDF/网页/知识库）。
- 分块（chunking）+ embedding + 向量检索 + 重排。
- 输出带引用答案，确保可追溯。

### 第 3-4 周：升级到 Agentic RAG
- 使用 `LangGraph` 拆分节点：问题分类、查询改写、检索策略选择、回答生成、自检/重试。
- 加入工具化能力：元数据过滤、多路检索（dense + keyword）、失败回退策略。

### 第 5 周：前端体验完善
- 聊天流式输出、引用跳转、会话历史。
- 用户反馈入口（👍/👎 + 原因）用于后续评估与迭代。

### 第 6 周：评估与可观测
- 离线评测：准确率、召回率、引用准确率。
- 线上追踪：链路 tracing、延迟与成本监控。

### 第 7 周：生产化与安全
- 鉴权、限流、敏感信息脱敏、注入防护。
- 灰度发布、告警、回滚与备份策略。

## 首批可执行任务（建议按顺序）

1. 初始化目录：`/backend`、`/frontend`、`/infra`、`/docs`。
2. 后端先做 3 个 API：`/ingest`、`/chat`、`/chat/stream`。
3. 准备至少 50 条评测问题，先跑通基线 RAG。
4. 基线达标后再加 Agent 节点，不要反过来。

## 参考文档（官方）

- FastAPI: https://fastapi.tiangolo.com/
- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- Next.js: https://nextjs.org/docs
- OpenAI Embeddings: https://developers.openai.com/api/docs/guides/embeddings
- Qdrant: https://qdrant.tech/documentation/
- LangSmith Observability: https://docs.langchain.com/langsmith/observability

## 参考开源项目

- OpenRAG: https://github.com/langflow-ai/openrag
- FastGPT: https://github.com/labring/FastGPT
