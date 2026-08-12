# Token 测算体系（token-meter）

量化"框架各文件占多少 token / 优化省了多少"，用**同一把尺子量前后**，让 token 优化可度量、可验证、可回归。

## 为什么需要

token 优化前靠"感觉"和"行数"判断，不可靠：
- 行数 ≠ token（中文 ~1.5 token/字，英文 ~0.25 token/词，代码 ~0.3 token/字符，mermaid/emoji 各异）
- "省多少"取决于场景（纯后端 CLI vs 全栈 DDD 走的分支不同）
- 不区分"每轮都花"和"按需才花"会得出错误结论

本体系用 `tiktoken`（cl100k_base 分词器）精算 + 场景矩阵，把 token 变成**可对比的数字**。

## 精度声明（重要）

- 分词器用 `cl100k_base`（GPT 系列 BPE），**与 Claude 实际 token 有偏差**（Claude 用自己的 BPE）
- 但**前后对比用同一分词器**，相对优化比例（省 X%）**可信**，绝对值仅供参考
- 若需绝对精确，用 API 返回的 `input_tokens` 校准（成本高，不纳入本工具）

## 测算层次与边界（务必读懂——否则误用）

本工具是**层 A（结构效率）**，不是**层 B（真实计费）**。两者不等价：

| 层 | 测什么 | 怎么测 | 回答 |
|----|--------|--------|------|
| **A 结构效率**（本工具） | 框架产出的文件 token | tiktoken 静态算 | "提示词架构瘦了多少" |
| **B 真实计费**（需另测） | API 实际 usage | 真实发请求采集 | "账单少了多少" |

**A 是理论上限，B 是实际效果。A ≠ B**，差距来自三个静态估算碰不到的东西：

### 1. Prompt Cache（最大失真源）

Claude Code 有 5 分钟 TTL 的 prompt cache，计费非线性：

| 类型 | 倍率 |
|------|------|
| cache write（首次/缓存失效后）| 1.25× 基础价 |
| **cache read（命中）** | **0.1×**（基础的十分之一）|
| 不缓存 | 1× |

**影响**：orchestrator 是稳定常驻的，大概率命中缓存 → 每轮只付 0.1×。
本工具报告"主对话每轮省 2771 tok"是**基础价等效**；若该部分命中缓存，实际计费只省 ~277 tok（2771 × 0.1），**差一个数量级**。

**反直觉结论**：优化"稳定常驻"内容（命中缓存的）实际省得少；优化"对话历史/工具结果"（不命中缓存的）才真省。低频分支外置到 handbook 的收益**反而更接近真实**——因为它从"常驻命中缓存"变成"触发时按工具结果计（不缓存）"，计费模型变化更复杂。

### 2. 对话历史累积

真实 input token = 系统提示词 + **之前所有轮次的历史** + 工具结果 + 当前输入。
orchestrator 21000+ tok 看着大，但 20 轮对话的历史可能 50000+ tok，优化的那点在历史面前变小。本工具**不测历史**（与框架优化无关，但影响真实账单）。

### 3. 工具定义

每次请求带所有可用 tool 的 JSON schema（Read/Write/Bash/Agent…），固定开销。本工具不测（优化前后一样，不影响对比结论）。

### 各文件的缓存特性（理解 A/B 差距用）

| 文件类型 | 缓存特性 | 静态 token vs 计费 token |
|----------|---------|------------------------|
| orchestrator（主对话常驻）| 稳定 → 多数命中 cache read | 计费 ≈ 静态 × 0.1（每轮）|
| agent 人设/skill（subagent）| 5min TTL 内重复派才命中 | 不稳定，计费 ≈ 静态 × 0.1~1.25 |
| handbook/references（Read 工具结果）| 工具结果通常不缓存 | 计费 ≈ 静态 × 1 |

## 层 B：真实计费怎么测（补全方案）

层 A 证明"提示词瘦了"，要知"账单省多少"需真实采集：

**✅ 已实现：`trace.py`（解析已落盘的 session usage）**

Claude Code 每次 LLM 调用的 usage（input/output/cache_read/cache_write）**已自动记录**在 session jsonl 里：
```
~/.claude/projects/<项目编码名>/<uuid>.jsonl
```
subagent（Agent 工具派的角色）的 usage 也在同一个主 session 文件里，无需聚合子文件。

`trace.py` 解析这些已记录的 usage，按计费倍率汇总，支持两 session A/B 对比：

```bash
# 单 session 分析（看真实 token 分布 + 缓存命中率）
python tools/token-meter/trace.py ~/.claude/projects/<项目>/<uuid>.jsonl

# 前后对比（核心：优化前 session vs 优化后 session）
python tools/token-meter/trace.py --before <旧session>.jsonl --after <新session>.jsonl --report tools/token-meter/reports/trace-report.md
```

**找 session 文件**：`ls -t ~/.claude/projects/<项目>/*.jsonl | head -1`（按时间取最新）

**计费倍率**（可在 `--rate-output` 覆盖）：input×1.0 / output×5.0 / cache_write×1.25 / cache_read×0.1

**怎么造可比的两个 session**（用户操作）：
1. 项目 A：`.claude` 切旧版（`git -C .claude checkout <旧tag>`），跑 `/goal-d <需求>` 到完成 → session A
2. 项目 B：`.claude` 用新版，跑 `/goal-d <同一需求>` 到完成 → session B
3. `trace.py --before A --after B` → 对比报告
4. ⚠️ 可比前提：**同一需求/同模型**；LLM 非确定，两次 turn 数会不同，报告含"每轮均 token"供归一化参考

> Claude Code 是交互式 CLI，跑完整 agent 流程需手动驱动（不能脚本全自动）。若只测单 agent 人设 token，可让单个 agent 处理同一小任务（如"让 code-planner 分析这段需求"），turn 少、噪音小。

**其他方法（参考）**：

**方法 1：Claude Code 会话级**

**方法 2：API 级（最准）**
- 用 Anthropic API 直接调（绕过 Claude Code），读 `response.usage`：
  - `input_tokens` / `output_tokens`
  - `cache_creation_input_tokens`（write）
  - `cache_read_input_tokens`（read）
- 能精确区分缓存命中与否，算出真实计费

**方法 3：代理拦截（折中）**
- 在 Claude Code 与 API 之间加代理，记录每次请求的 usage
- 不改框架，但需配代理环境

> 层 B 的成本/不稳定性较高（要跑真实流程、LLM 输出非 deterministic），**建议作为阶段性校验**（如重大优化后跑一次），而非每次优化都跑。日常优化用层 A 快速迭代，定期用层 B 校准。

## 什么时候用哪层

| 场景 | 用层 |
|------|------|
| 日常优化迭代（改了提示词，快速看瘦没瘦）| **A**（本工具，秒级）|
| 判断优化方向（哪些是高频/低频）| A |
| 向别人证明"真的省钱了" | **B**（真实账单）|
| 缓存策略调优（稳定 vs 变动）| B（A 看不出缓存效果）|
| 重大优化后的最终验收 | A 先行 + B 校准 |

## 三层指标（token 不是"一个数"）

不同层面的"省"完全不同，必须分开算：

| 层 | 是什么 | 花法 | 优化收益 |
|----|--------|------|---------|
| **① 主对话常驻** | orchestrator 系统提示词 | **每轮对话**都花 | 省 Δ × 对话轮数 |
| **② Agent 派发** | agent 人设 + 挂载的 skill SKILL.md | 每次 `Agent()` 调用花一次 | 省 Δ × 派发次数 |
| **③ 按需外置** | handbook / references | 平时 **0**，触发时才花 | 平时全省，触发时花一次 |

> 核心洞察：**①②是高频（必然花），③是低频（按需花）**。把低频内容从①②挪到③ = 平时省、触发时才花。净收益 = 常驻省 × 频率 − 外置花 × 触发率。低频分支触发率 ≪ 1，所以净收益正。

## 场景矩阵（"省多少"取决于场景）

| 场景 | 走的分支 | 触发的外置文件 |
|------|---------|---------------|
| **纯后端 CLI**（快速模式） | 快速模式，无原型/无 DDD/无服务依赖 | 无 → 外置全不读，省 100% |
| **全栈 Web**（标准 SOP + DDD） | 标准 SOP，DDD，原型 | ddd-tactics |
| **后端 API + DB**（服务依赖） | 标准 SOP | e2e-external-deps |
| **存量项目改动** | 存量模式 | stock-mode |

同一份优化，纯后端 CLI 场景省得最多（外置全不读），全栈 DDD 场景省得少（要读 ddd-tactics）。

## 用法

```bash
# 单 ref 快照（算当前 HEAD 的 token 分布）
python tools/token-meter/scan.py --ref HEAD

# 前后对比（核心用法：量化优化省了多少）
python tools/token-meter/scan.py --before feat/review-gate-and-shared-acceptance --after HEAD

# 指定输出报告路径
python tools/token-meter/scan.py --before <旧ref> --after <新ref> --report docs/token-report.md
```

## 算法

1. `git show <ref>:<path>` 读该 ref 的文件内容（无需 checkout，跨分支对比）
2. `tiktoken.cl100k_base` 算每个文件 token 数
3. 解析每个 agent 的 frontmatter `skills:` 字段 → agent 派发负载 = 人设 token + Σ 挂载 skill 的 SKILL.md token
4. 场景必然 token = 主对话常驻（orchestrator）+ Σ 场景用到的 agent 派发负载 + Σ 场景触发的外置文件
5. 前后对比 = 优化后场景必然 token − 优化前场景必然 token（负数 = 省了）

## 测什么 / 不测什么

| 测（框架能控的） | 不测（与优化无关） |
|------------------|-------------------|
| orchestrator 系统提示词 | 模型输出 token |
| agent 人设 + 挂载 skill | 用户输入 |
| handbook / references | 运行时读的业务文件（PRD/代码/测试报告） |
| | 工具调用开销 |

不测的部分优化前后一样，不影响"省多少"的对比结论。
