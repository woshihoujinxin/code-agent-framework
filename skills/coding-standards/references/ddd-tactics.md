# DDD 战术模式（领域驱动设计）

> **何时读本文件**：仅当主Agent 注入 `方法论：DDD`（标准SOP + 业务规则复杂：领域概念密集/多状态流转/多模块交互/明确业务规则）时。快速模式 / BugFix / 存量模式 / 纯后端简单项目**不读本文件**。
>
> 触发后：Planner 做领域建模（design.md「领域建模」段 + 四层目录骨架），Dev 按本文件战术分层写码，quality tester 增加领域建模审查维度。

## 分层与依赖方向

Domain（实体/值对象/聚合/仓储接口/领域服务）→ Application（应用服务/用例编排）→ Interface（API/CLI）→ Infrastructure（仓储实现/外部依赖）；依赖方向只允许外层指向内层，**Domain 层零外部依赖**。

## 目录骨架（强制，建项目骨架时照此创建）

`src/` 按四层固定目录组织：

```
src/
├─ domain/          # 实体/值对象/聚合/仓储接口/领域服务（Domain 层，零外部依赖）
├─ application/     # 应用服务/用例编排（依赖 domain，被 interface 依赖）
├─ interface/       # API/CLI/控制器/路由（依赖 application/domain）
└─ infrastructure/  # 仓储实现/DB/外部客户端（实现 domain 的仓储接口）
```

依赖方向：`interface → application → domain`；`infrastructure` 实现 `domain` 的接口。**禁止** domain 引用其他任何层符号。

## 战术构件

- **实体（Entity）**：有唯一标识与生命周期，状态变化必须通过领域方法表达（不暴露 setter 裸改）
- **值对象（Value Object）**：无标识、不可变，通过值相等比较；优先建模为值对象而非基本类型（金额/地址/时间区间）
- **聚合（Aggregate）**：聚合根是外部访问的唯一入口，聚合边界内强一致；跨聚合的修改经应用服务协调，不直接穿透对象图
- **仓储（Repository）**：接口定义在 Domain 层，实现在 Infrastructure 层；调用方只依赖接口不依赖具体实现

## 禁止反模式

- 贫血模型（实体只有 getter/setter 无行为）
- Infrastructure 类型泄漏进 Domain
- 聚合根直接操作其他聚合的内部对象

## 命名

聚合根/实体用业务术语（与 PRD 领域词汇表一致），禁止技术化命名（如 `DataModel`、`Manager`）。
