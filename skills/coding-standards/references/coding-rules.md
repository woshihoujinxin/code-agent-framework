# 编码规范（Dev / 审码角色必读）

> **受众：写代码或审代码的角色**——`code-dev-backend` / `code-dev-frontend` / `code-reviewer`（审查时以此为准）。
> Tester **不需要读本文件**（Tester 按五维验收判卷，见 `test-acceptance-standards.md`）。

---

## 1. 命名约定

- **见名知意**：变量/函数/文件名禁用无意义缩写（`x`、`tmp`、`data2`），用完整词或公认缩写（`url`、`id`、`cfg`）
- **一致性**：一个项目内只用一种命名风格（Python 用 `snake_case`，JS/TS 用 `camelCase` 类型用 `PascalCase`）
- **布尔值**用 `is_/has_/should_` 前缀；**函数名用动词**开头（`get_/create_/update_/delete_`）

## 2. 项目结构

- 源码 → `src/` 或 `app/`（沿用项目既有结构，不新建第二套）
- 测试 → `tests/`；测试报告 → `tests/reports/`
- 工程文档 → `docs/`
- **禁止在仓库根目录创建代码文件**（仅 `README.md`、`.gitignore`、包管理文件允许）
- **`references/` 目录边界**：仅作架构研究参考，Dev 不执行/修改/依赖，Tester 不测试其内容（详见 contract-shared §2）

## 3. 设计模式偏好

- **单一职责**：一个函数做一件事，≤ 50 行；参数 ≤ 4 个，超出则封装为对象或拆分
- **DRY**：重复 ≥ 2 次的逻辑必须抽取为函数/方法
- **显式优于隐式**：复杂逻辑加注释；公共接口加文档串
- **早返回**：用 guard clause 减少嵌套（避免超 3 层缩进）

### 3b. DDD 战术模式（仅 `方法论：DDD` 模式注入时读手册）

> **何时读手册**：主Agent 注入 `方法论：DDD`（标准SOP + 业务规则复杂）时，**读 `ddd-tactics.md`** 按其四层目录骨架（domain/application/interface/infrastructure，Domain 零外部依赖）+ 战术构件（实体/值对象/聚合/仓储）+ 禁止反模式执行。快速模式 / BugFix / 存量模式 / 简单项目**不读**（多数项目用不到，避免死重 token）。

## 4. 测试约定（Dev 写单测的规范）

- **五维验收标准**（开发前必读）：`test-acceptance-standards.md` 是"什么样的代码才算通过"的权威定义，开发前必读对齐 Q/B/S 验收维度，避免测试阶段返工。
- 外部依赖（文件/网络/数据库/外部 API）的读操作必须**包裹异常处理**并定义降级行为
- 外部输入必须有**空值/边界校验**
- 资源（文件句柄/连接）在异常路径也要释放（用 `with`/`try-finally`/`defer`）
- 单元测试 mock 外部依赖；E2E 测试用独立环境
- **单元测试强制**：位置 `tests/unit/test_{TASK_ID}_{name}.{ext}`；命名 `test_{用例编号}_{场景}`；**必须覆盖测试契约的 F/B/S 用例**（每条对应一个单测函数）；未覆盖的须在自检报告 `tests/reports/{TASK_ID}-selfcheck-*.md` 声明理由

## 5. 大文件分段读取（硬规则——渐进式加载）

> **何时生效**：任何文档/报告 > 10KB 时。防止全量读入把大文件（跨版本累积的 feature-spec/lessons-learned/dev-plan/报告）整体塞进 context。

- **先 Grep 定位，再分段 Read**：`Grep` 锚点（如 `^## TASK-`、`测试契约`、`TASK_IDx`）找到目标行号 → `Read` 用 offset/limit 只取目标范围，**禁止整读全文**
- **只读自己需要的段**：Dev/Tester 只读本任务的契约段/自检段，不读整版本；lessons-learned 只 Grep 与本任务 TASK_ID 相关的条目
- **收尾归档**：已验收的旧版本内容在 `docs/archive/v{version}/`，运行时文件只留当前版本——发现运行时文件仍有旧版本残留时提示归档

---

> 通用模板说明：若本文件留空/未按项目填充，Agent 会使用通用最佳实践。
