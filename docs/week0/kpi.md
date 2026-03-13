# KPI 与验收标准（Week 0）

## 指标定义

1. 回答正确率（Answer Correctness）
- 定义：人工评审中“回答与标准答案语义一致”的比例。
- 公式：`correct_count / total_count`
- Week 0 门槛：`>= 0.80`

2. 引用命中率（Citation Hit Rate）
- 定义：回答中包含引用，且引用文档可支持答案结论的比例。
- 公式：`valid_citation_count / answered_count`
- Week 0 门槛：`>= 0.90`

3. P95 延迟（P95 Latency）
- 定义：95 分位端到端响应时延（秒）。
- Week 0 门槛：`<= 8s`

4. 单问成本（Cost per Query）
- 定义：一次问答平均模型与检索成本。
- Week 0 门槛：`<= ¥0.20`（或等值美元）

## 验收规则

1. 评测样本数在 50-100 条之间。
2. 每条样本必须有标准答案（gold answer）。
3. 每条样本必须有来源引用字段（source_reference）。
4. 四项 KPI 全部达到门槛后，才进入第 1 周工程实施。

## 统计频率

1. 开发阶段：每日一次离线跑分。
2. 提测阶段：每次重要改动后重新跑分并记录。
