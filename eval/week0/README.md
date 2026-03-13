# Week 0 评测集说明

## 文件说明

1. `qa_goldens_seed.csv`：第 0 周种子问答集（50 条，含标准答案与来源字段）。
2. `rubric.md`：人工打分规则。

## 使用方式

1. 先用 `qa_goldens_seed.csv` 跑通最小离线评测流程。
2. 用真实用户问题逐步替换 seed 问题，保持总量 50-100 条。
3. 每次替换后，更新 `source_reference`，确保答案可追溯。

## 字段定义

- `id`: 样本编号
- `question`: 用户问题
- `gold_answer`: 标准答案
- `source_reference`: 来源文档（文件或章节）
- `intent`: 意图类型（factoid/process/link）
- `difficulty`: 难度（easy/medium/hard）
- `must_cite`: 是否必须输出引用（true/false）
