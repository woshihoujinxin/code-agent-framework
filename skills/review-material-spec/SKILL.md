---
name: review-material-spec
description: |
  评审材料规范与齐备性 gate。定义 docs/reviews/{version}/ 版本目录结构、各产物由谁产出、
  版本号约定、三件齐备校验清单（research.md 兼任设计草案）。是 goal-research/goal-review/goal-spec 三者的单一真相源——
  模板变了只改本文件，命令与编排器引用它，不另维护第二份清单。
---

# 评审材料规范（review-material-spec）

> **本文件是评审材料的单一真相源。** 目录结构、产出角色、gate 清单都在这里。
> `goal-research`（调研产出落盘）、`goal-review`（评审前齐备性校验）、`goal-spec`（散素材按规范归位+格式化）三者都读本规范，不各自另定。

## 1. 核心约定：版本目录

每次评审 = 一个版本目录 `docs/reviews/{version}/`。从调研起，所有评审素材都落进**同一目录**，评审基于目录内产物进行，不东拼西凑。

```
docs/reviews/{version}/
├── research.md          # 调研结论（图为主）= 设计草案  ← goal-research 产出（兼任评审方案输入）
├── requirement.md       # 精简需求                   ← goal-research 产出
├── design-draft.md      # （可选）更细方案草案         ← Planner 产出（research.md 已兼任草案，需细化时才单独产）
├── prototype/           # 原型产物                   ← Prototype Builder 产出
│   ├── index.html / cli.md   # 原型本体
│   ├── DESIGN.md             # 设计令牌
│   ├── critique.md           # 独立审查
│   └── mock-cli.*            # 可运行模拟器（如有）
├── pm-init.md           # PM 背靠背初审稿（可选）     ← 评审期产出
├── planner-init.md      # 架构师背靠背初审稿（可选）  ← 评审期产出
├── prototype-presentation.md  # 原型演示稿（可选）  ← 评审期产出
└── review-meeting.md    # 评审纪要（评审后产出）     ← goal-review 产出
```

## 2. 版本号约定

- `{version}` 是**人工预声明的目标版本号**（如 `v0.0.11`），仅作目录名与材料标签。
- **不绑 git tag**——评审阶段是纯文件系统层面的事，git 管理（tag/分支）是产出代码之后的事。
- 一个 version 目录对应一次评审闭环。**评审不过需重做时，覆盖原文件、不新增、不留中间过程**（详见 §7 重做一致性规则）。同版本目录永不另建、不追加轮次后缀。
- version 来源：命令参数首位置提供（`/goal-research v0.0.11 ...`），未提供则编排器 `AskUserQuestion` 询问。

## 3. 产出角色矩阵

| 产物 | 产出角色 | 产出时机 | 命令 |
|------|---------|---------|------|
| `research.md` | code-researcher | 调研期（兼任设计草案） | goal-research |
| `requirement.md` | code-researcher | 调研期 | goal-research |
| `design-draft.md`（可选） | code-planner | 评审前（仅当 research 草案需细化时） | goal-review 素材准备段 |
| `prototype/*` | code-prototype-builder + critic | 评审前 | goal-review 素材准备段 |
| `pm-init.md` | code-product-manager | 评审期（背靠背初审） | goal-review |
| `planner-init.md` | code-planner | 评审期（背靠背初审） | goal-review |
| `prototype-presentation.md` | code-prototype-builder | 评审期（演示稿） | goal-review |
| `review-meeting.md` | 评审编排器 | 评审后 | goal-review |

> **design 角色定位（重要）**：调研产出的 `research.md`（技术方案：架构图/实体/状态/时序图 + 推荐方案）**即设计草案**，评审直接审它。拍板后才落正式 `design.md`（开发期 Planner 产出，落 `docs/design.md`）。`design-draft.md` 仅当 research 草案需更细方案时由 Planner 单独补，**非 gate 必备**。**不要把正式 design 当评审输入**——那样评审就变成事后追认。

## 4. 三件齐备 gate（评审前强制校验）

`goal-review` 进评审前，按下表逐项 `Glob/Read` 校验 `docs/reviews/{version}/` 下必备件。**缺任一项 → 拒绝进入评审，报告缺哪个 + 该跑什么命令补**，不降级放行。

> **research.md 兼任设计草案**：调研产出的技术方案即评审方案输入，gate 不另要求 design-draft.md（其可选，需细化方案时 Planner 单独补）。

| 必备输入 | 校验路径 | 缺则提示 |
|----------|---------|---------|
| 调研 + 设计草案 | `research.md` | "缺调研/技术方案 → 先跑 /goal-research {version}" |
| 需求 | `requirement.md` | "缺需求 → 先跑 /goal-research {version}" |
| 原型 | `prototype/` 目录非空 | "缺原型 → 先走原型子流水线（/goal-review 素材准备段）" |

> 纯算法/无交互项目可标注「无原型」跳过原型项——需在 `requirement.md` 内显式声明 `prototype: none`，gate 据此放行。

校验全过 → 输出 `REVIEW_PACKAGE = [版本目录内全部产物路径]`，进入评审会议。
评审纪要落 `docs/reviews/{version}/review-meeting.md`，结论字段（通过/有条件通过/不通过）解锁下游开发。

## 5. 文件 frontmatter 规范（goal-spec 格式化用）

每个产物文件头部应有规范 frontmatter，`goal-spec` 归位时补齐：

```markdown
---
version: {version}
artifact: {research|requirement|design-draft(可选)|prototype|review-meeting|...}
producer: {code-researcher|code-planner|code-prototype-builder|...}
review_batch: {version}
---
```

> frontmatter 是机器可读的溯源元数据，便于编排器扫目录判断齐备性，也便于跨版本检索。

## 6. 变更本规范时

本文件是单一真相源。改目录结构/产出角色/gate 清单时：
- 只改本文件；
- `goal-research` / `goal-review` / `goal-spec` 三编排器引用本规范的字段名，不复制清单正文——这样模板变了不用改三处。

## 7. 重做一致性规则（评审不过 → 覆盖，不留中间过程）

**核心原则**：一个 version 目录 = 一套材料，永远只反映最新一轮状态。评审不通过需重做（重新调研/重产素材/修原型/复审）时：

- **覆盖原文件**：`research.md` / `requirement.md` / `prototype/*` / `pm-init.md` / `planner-init.md` / `review-meeting.md`（及可选 `design-draft.md` 如存在）全部**同名覆盖**，不新增文件、不追加 `-r2`/`-v2` 后缀、不另建目录。
- **不留中间过程**：上一轮被否的材料不保留、不归档到同目录。**git 历史是唯一的版本回溯通道**（要查旧版用 `git log` / `git show`，不在工作目录留中间产物）。
- **纪要覆盖但记轮次**：`review-meeting.md` 覆盖时，在「基本信息」段记一行「评审轮次：第 N 轮；上一轮决议：不通过（{原因}）」——不丢关键决策，但不留中间纪要文件。
- **gate 仍校验**：重做后重跑三件齐备 gate，齐了才进新一轮评审。

> 这条规则保证「一个版本一套材料」的一致性——任何人看 `docs/reviews/{version}/` 拿到的都是当前最新、唯一的评审材料，不存在「多份到底哪份为准」的歧义。`goal-research`（重做调研）/`goal-review`（重做评审）发现 version 目录已存在时，一律按覆盖处理，不新建。
