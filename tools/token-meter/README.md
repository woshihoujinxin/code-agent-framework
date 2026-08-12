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
