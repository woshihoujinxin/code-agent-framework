# 编码项目多智能体开发系统

基于 RALPH 循环的通用编码 Agent 协作框架，在 Claude Code 中运行。

## 整体流转：三层闭环怎么转起来

> 系统是 **loop 套 loop**：外层持续吞需求，中层逐批消化任务，内层修正缺陷，外加自进化回路。
> 角色间靠 **文件异步交换**（不直接对话），由 **编排器** 按 `dev-plan.md` 状态机（⏳🔄✅⚠️）推进。

```
┌═══ 外层：项目大循环（永不退出，持续吞需求）═══════════════════════┐
║   👤 用户(随时追加需求)                                            ║
║      │ req                                                        ║
║      ▼                                                            ║
║   [PM] ──prd.md(用户故事US-N)──→ [架构师]                         ║
║                 │  feature-spec.md(测试契约F/B/S/E/Q)             ║
║                 │  dev-plan.md(⏳🔄✅⚠️) + smoke-checks.md        ║
║                 ▼                                                 ║
║   ┌═══ 中层：批次循环（master 逐批消化 ⏳）══════════════════╗   ║
║   ║   取一批 ⏳                                                ║   ║
║   ║      ├── [FE Dev] ∥ [BE Dev]  ◄──契约+PRD+lessons        ║   ║
║   ║      │      写代码+单测(tests/unit)+selfcheck             ║   ║
║   ║      │   ◆ 冒烟关卡(跑单测+查selfcheck存在)               ║   ║
║   ║      │      └ 不过→resume Dev 修                          ║   ║
║   ║      ▼                                                    ║   ║
║   ║   [correctness][quality][robustness][security][e2e]       ║   ║
║   ║      五维并行  ◄──契约用例+PRD+selfcheck                  ║   ║
║   ║      │ 测试报告(契约验证表 + P/F + 标签)                  ║   ║
║   ║      │                                                    ║   ║
║   ║   ┌── 内层：修正循环(≤3轮) ──────────┐                    ║   ║
║   ║   │  FAIL→resume Dev                 │                    ║   ║
║   ║   │    修代码+补单测+更selfcheck      │                    ║   ║
║   ║   │    →resume Tester重测            │                    ║   ║
║   ║   │      (取最后一次判定)             │                    ║   ║
║   ║   └──────────────────────────────────┘                    ║   ║
║   ║      ├── 全PASS→dev-plan标✅→下一批 ─┐                    ║   ║
║   ║      └── 3轮仍FAIL→升级               │                    ║   ║
║   ║                │ upgrade-issue.md    │                    ║   ║
║   ║                ▼                     │                    ║   ║
║   ║          [PM]评估→[架构师]重拆→新⏳──┘                    ║   ║
║   ╚══════════════════════════════════════════════════════════╝   ║
║                 ▼                                                 ║
║   [code-sage] ◄── 所有报告 + metrics                              ║
║      │ 提炼高频标签为防错规则                                      ║
║      ▼                                                            ║
║   coding-standards(自进化规则)                                    ║
║      │                                                            ║
║      ▼                                                            ║
║   回到顶部吞下一个需求 —— 规则已增强，同类错误下次递减 ───────────┘
└═══════════════════════════════════════════════════════════════════┘
```

### 三个回流点 = 闭环所在

| 回流 | 触发 | 路径 |
|------|------|------|
| **修正**（内层） | 测试 FAIL | Tester → resume Dev → 补单测+更自检 → 重测（≤3轮） |
| **升级**（中层补救） | 3 轮仍 FAIL | → PM 评估 → 架构师重拆 → 新 ⏳ 任务入队 |
| **自进化**（跨需求） | 收尾 / 每 5 批 | code-sage 提炼标签 → coding-standards → 下次全员读，同类错误递减 |

> 角色间**不直接通信**——写文件 + 读文件（见文末「项目文件体系」）。这是异步解耦、上下文不爆的关键。

## 两条流程

| | 开发版 | 全流程版 |
|---|---|---|
| 主Agent | `dev-quality-orchestrator.md` | `delivery-orchestrator.md` |
| 阶段 | 产品分析 → 计划 → 前后端开发 → 五维测试 | 计划 → 开发 → 审查 → 构建 → 校验 |
| 子Agent | PM + 架构师 + FE/BE Dev + Tester×5 | 架构师 + FE/BE Dev + Reviewer + Builder + Validator |
| 产出 | 可运行的代码 | 可部署的制品 |

### 开发版：需求 → 代码

```
你提需求 → PM 分析写PRD → 架构师 拆任务 → 前后端并行开发 → 五维测试 → 修正循环 → 完成
```

### 全流程版：需求 → 制品

```
你提需求 → 架构师 拆任务 → 前后端开发 → Reviewer 审查 → Builder 构建 → Validator 校验 → 制品就绪
```

### 工作流路由（B1）— 需求进门先分级

| 模式 | 判定 | 处理 |
|------|------|------|
| **标准SOP** | 多模块 / 多端 / 复杂状态 / 拿不准 | 现有全流程 |
| **快速模式** | 小需求（≤10 源文件 / 单模块 / 无多端 / 无复杂状态） | 压缩版循环：PM 简洁PRD + 架构师 ≤3 大任务 + 单 Dev + 五维 1 轮 + 修正 ≤2 轮；**测试契约照常产**（feature-spec F/B/S/E/Q 共享上下文保证不变） |
| **BugFix** | 明确 bug 描述 | resume 相关 Dev + 受影响维度重测，不重走 PM/Planner |

### 原型子流水线（A3）— Web 需求自动出高保真原型

PRD 写完后自动判断：场景含前端/Web → `code-prototype-builder` 产出 `docs/prototype/index.html` + `DESIGN.md`（视觉基准：前端 Dev 对齐令牌、quality tester 核查视觉一致性）；纯 CLI/API → SKIP 不浪费。交付版尾端再加 `code-export-specialist` 导出 HTML/PDF/PPTX/ZIP 到 `exports/`（A5）。

---

## 安装（一键）

框架就是 `.claude/` 目录的内容。在你的项目里 git clone 即装好：

```bash
cd my-project
git clone https://github.com/woshihoujinxin/code-agent-framework.git .claude
# 重启 Claude Code（加载新的 agents / commands / skills）
```

> 不想 `.claude/` 带嵌套 `.git`：clone 后 `rm -rf .claude/.git`
> **更新框架**：`cd my-project/.claude && git pull`（再重启 Claude Code）

clone 后 `.claude/` 自动包含 15 个 subagent、`/goal-d` `/goal-o` `/goal-init` 命令、两个编排器、3 个 skills（coding-standards / design-systems / prototype-templates）——**无需手动复制任何文件**。

**按项目调整编码规范**（可选）：编辑 `.claude/skills/coding-standards/SKILL.md` 的 §1–§4（命名/结构/模式/测试）。末段「自进化规则」由 code-sage 自动追加，不要手改。

---

## 使用

### 启动（一句话）

在项目里开 Claude Code，用 slash 命令，斜杠后跟需求：

```
/goal-d 用 Python 做个 Todo CLI，支持创建/查询/删除/标记完成    # 研发质量编排 → 高质量代码
/goal-o 做个 FastAPI 服务并打包成 Docker 镜像                  # 交付编排 → 可部署制品
```

也可以不写命令，直接描述需求，PM 会自动生成 PRD 再进入开发。

> `/goal-d` 走五维质量门（功能/质量/健壮/安全/E2E）产出代码；`/goal-o` 走审查→构建→校验链产出制品。两者区别见 `dev-quality-orchestrator.md` / `delivery-orchestrator.md` 开头。

### 执行流程

启动后主Agent 自动进入以下阶段：

**Phase 0 — 产品需求分析**
- 如果用户提供原始需求描述，启动 `code-product-manager` 编写 PRD
- 支持用户随时追加新需求，PM 追加到需求池

**Phase 1 — 计划**
- 架构师 读取需求文档
- 拆分为可独立验证的子任务
- 输出 `dev-plan.md` + `feature-spec.md`
- 搭建项目骨架

**Phase 2 — 逐批开发循环**

每批任务执行：

1. **前后端并行开发**：`code-dev-frontend` + `code-dev-backend` 并行编码
2. **冒烟检查**：验证代码至少能跑，不通过则回到 Step 1
3. **五维测试**：五个 Tester 并行审查（功能/质量/健壮/安全/E2E）
4. **修正循环**（≤3 轮）：Dev 修复 → Tester 重测
5. 全 PASS 后更新 `dev-plan.md`，向用户报告进度

**Phase 3 — 收尾**
- 统计迭代情况
- 输出完成报告
- 进入等待状态，持续接收新需求

---

## 角色体系

| 角色 | 文件 | subagent_type | 适用版本 |
|------|------|---------------|---------|
| 主Agent | `dev-quality-orchestrator.md` | —（主对话） | 开发版 |
| 主Agent | `delivery-orchestrator.md` | —（主对话） | 全流程版 |
| 产品经理 | `code-product-manager.md` | `code-product-manager` | 开发版 |
| 架构师 | `code-planner.md` | `code-planner` | 共用 |
| 前端开发 | `code-dev-frontend.md` | `code-dev-frontend` | 开发版 |
| 后端开发 | `code-dev-backend.md` | `code-dev-backend` | 共用 |
| 功能测试 | `code-tester-correctness.md` | `code-tester-correctness` | 共用 |
| 质量测试 | `code-tester-quality.md` | `code-tester-quality` | 共用 |
| 健壮测试 | `code-tester-robustness.md` | `code-tester-robustness` | 共用 |
| E2E测试 | `code-tester-e2e.md` | `code-tester-e2e` | 共用 |
| 安全测试 | `code-tester-security.md` | `code-tester-security` | 共用 |
| Reviewer | `code-reviewer.md` | `code-reviewer` | 全流程版 |
| Builder | `build-builder.md` | `build-builder` | 全流程版 |
| Validator | `artifact-validator.md` | `artifact-validator` | 全流程版 |
| 经验提炼 | `code-sage.md` | `code-sage` | 共用（自进化） |
| 原型构建师 | `code-prototype-builder.md` | `code-prototype-builder` | Web项目（A3） |
| 导出交付 | `code-export-specialist.md` | `code-export-specialist` | 全流程版（A5） |

> 注：两个版本都用 `code-dev-frontend.md` + `code-dev-backend.md`（前后端分离开发）；区别在全流程版多了 Reviewer/Builder/Validator 制品环节。

---

## 五维质量闸门

```
开发完成
   │
   ├── 功能正确性：对照 feature-spec.md 验收标准逐条 PASS/FAIL
   ├── 代码质量：审查命名、设计模式、复杂度、重复代码
   ├── 健壮性：审查空值、边界、异常处理、资源释放
   ├── 安全性：攻击者视角审查注入、越权、敏感数据、配置、依赖
   └── 端到端：验证完整用户流程和系统集成
   │
   ▼
 全PASS → ✅ 完成
 有FAIL → Dev 修正 → 重测 → ≤3轮 → 问题升级
```

### 测试维度说明

| 维度 | 职责 | 测试方式 |
|------|------|----------|
| **功能正确性** | 验证功能是否按规格实现 | 静态分析代码逻辑 |
| **代码质量** | 审查代码可读性和设计 | 静态代码审查 |
| **健壮性** | 验证边界条件和异常处理 | 静态分析 + 边界场景检查 |
| **安全性** | 以攻击者视角查可利用漏洞 | 静态审计 + 依赖扫描 |
| **端到端** | 验证完整用户流程 | 实际执行 CLI/API 测试 |

---

## 项目文件体系

运行时会在代码仓库中生成：

| 文件 | 作用 | 谁写 |
|------|------|------|
| `docs/prd.md` | 产品需求文档（需求池，含「视觉意图」段） | 产品经理 |
| `docs/dev-plan.md` | 任务状态追踪 | 架构师 创建，主Agent 更新 |
| `docs/design.md` | 架构设计（技术决策记录+模块架构图+实体/ER+时序图+状态机+共享知识+领域建模） | 架构师 |
| `docs/architecture.md` | 全局架构设计（复杂项目拆分：上下文划分+模块图） | 架构师 |
| `docs/feature-spec.md` | 每个任务的功能规格+测试契约 | 架构师 |
| `docs/lessons-learned.md` | 跨任务经验积累 | Dev（修正后更新） |
| `docs/prototype/` | 高保真原型 + DESIGN.md（视觉基准，A3） | 原型构建师（Web项目） |
| `exports/` | 导出交付物（HTML/PDF/PPTX/ZIP，A5） | 导出专家（交付版） |
| `docs/main-log.md` | 全流程日志 + checkpoint | 主Agent |
| `docs/upgrade-issue-*.md` | 问题升级需求文档 | 主Agent（3轮修复失败时） |
| `tests/reports/` | 测试报告目录 | Tester×5 |
| `tests/unit/` | 单元测试 | Dev（覆盖契约 F/B/S 用例） |
| `tests/reports/{TASK_ID}-selfcheck-*.md` | Dev 自检报告（声明契约用例覆盖） | Dev |

---

## 核心机制

### 上下文隔离
- 主Agent 不读子Agent产出内容，只看 `PASS/FAIL` 判定行
- 子Agent 每次必读文件从头读，不假设外部状态
- 子Agent 输出极简（PASS 时只返回一行）

### Resume 机制
- 修正循环 **resume 同一个 Agent**（保留开发上下文）
- 跨任务 **新建 Agent**（旧上下文是噪音）

### 经验积累
- `lessons-learned.md` 是跨任务知识传递的唯一通道
- Dev 在修正后更新，遵循三条抽象原则

### 问题升级
- 3 轮自动修复仍未通过时，自动触发升级流程
- PM 评估需求是否需要调整 → 架构师 拆解升级任务 → 加入开发队列

### 失败分类路由（B5）
- Tester FAIL 报告加「失败分类：实现Bug / 测试Bug / 契约Bug / 混合」
- 编排器按分类分流：契约Bug→架构师改 feature-spec 契约；测试Bug→Tester 复核；实现Bug→Dev 修复

### 上下文压缩
- 每 N 批后自动 checkpoint 到 `main-log.md`
- 支持会话中断后从 checkpoint 恢复

---

## 演示

`demo-todo-cli.md` 是一个完整的演练脚本，可直接复制到 Claude Code 中逐段执行，体验多Agent 协作开发 Todo CLI 工具的全流程。

---

## 示例

```
用户：用 Python 实现一个 Todo API，支持创建/查询/删除/标记完成

主Agent 调度：
  Phase 0: PM 分析需求 → docs/prd.md

  Phase 1: 架构师 拆分 →
    TASK01 数据模型 + 存储层
    TASK02 创建 + 查询 API
    TASK03 删除 + 标记完成 API
    TASK04 错误处理 + 参数验证

  Phase 2: 逐批开发 →
    TASK01: FE Dev + BE Dev → 冒烟检查 → 五维测试 → ✅ PASS (1轮)
    TASK02: FE Dev + BE Dev → 功能FAIL → 修正 → 重测 → ✅ PASS (2轮)
    TASK03: FE Dev + BE Dev → 五维测试 → ✅ PASS (1轮)
    TASK04: BE Dev → 质量FAIL → 修正×2 → ✅ PASS (3轮)

  Phase 3: 收尾 → 4/4 完成，平均 1.75 轮
```

---

## 自定义

### 调整测试维度

编辑对应 Tester 文件的检查维度表。例如增加性能测试：在 `.claude/agents/` 下新增 `code-tester-performance.md`，并在主Agent 的 Phase 2 Step 2 中增加第 5 个 Tester。

### 适配不同技术栈

1. 创建 `.claude/skills/coding-standards/SKILL.md`，写入实际规范
2. 四个 Tester 的检查项会自动引用该 skill

主Agent（`dev-quality-orchestrator.md`）在任何场景下不需要修改——它是纯编排层。

---

## 与幻灯片版本的关系

本套提示词从 `agents/` 目录的幻灯片版本泛化而来：

| 维度 | 幻灯片版本 | 编码版本 |
|------|----------|---------|
| 输入 | PPT素材 | 需求文档 |
| 规格文件 | page-design-guide.md | feature-spec.md |
| 产出 | index.html section | 代码文件（多个） |
| 测试维度 | 布局/美观/动画 | 功能/质量/健壮/E2E |
| 编排逻辑 | 完全一致 | 完全一致 |
