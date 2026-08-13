# 收尾手册（Phase 4，每版本收尾时才读）

> **何时读本手册**：Phase 3 全部任务完成后进入 Phase 4 时。**ROLES 判断**：导出(export) + code-sage 属增强角色——**精简模式跳过「指标与经验提炼段」**（只做基本统计 + 运行指南），**全能模式全执行**（含本手册全部步骤）。

全部任务完成后，按以下顺序执行：

## Step 1 测试汇总报告

1. 先追加 ⑥ 段头（仅一次）：
```
## ⑥ 项目收尾
```
2. 从 `tests/reports/results.json` 读每个任务的各维度判定 + 一句话结论（机器真源，最快最可靠）；无 results.json（旧项目）才回退 Grep 各 `tests/reports/{TASK_ID}-{dimension}.md` 的「一句话结论」行与判定行
3. 汇总写 `tests/reports/SUMMARY-{version}.md`（1 份，覆盖写）：
   ```markdown
   # {version} 测试汇总

   ## 总体结论
   {全部任务是否通过、系统能不能用——一句话人话结论}

   ## 各任务测试结果
   | 任务 | 一句话结论 | 功能 | 质量 | 健壮 | 安全 | E2E |
   |------|-----------|------|------|------|------|-----|
   | TASK01 | {该任务一句话结论} | ✅/❌ | ... | ... | ... | ... |

   ## 失败项（若有）
   - {TASK_ID} {维度}: {一句话问题 + 报告路径}
   ```
4. 判定列取各报告 `### 判定`（PASS→✅，FAIL→❌）
5. 统计各任务迭代情况，写入最终统计到 main-log.md：
```
- {yymmdd hhmm} 🏁 ════ 项目完成 ════
- {yymmdd hhmm} 🏁 全部 {N} 个任务完成
- {yymmdd hhmm} 📊 迭代统计：
  - 1次通过：{X} 个
  - 2次通过：{Y} 个
  - 3次通过：{Z} 个
  - 强制通过：{W} 个
```
日志：`- {yymmdd hhmm} 📄 测试汇总 → tests/reports/SUMMARY-{version}.md`

## Step 2 产出运行指南

让用户拿到就能跑——收尾必做，否则交付不完整：
- 读项目配置提取**真实**运行命令（master 读，不派 agent、不编造）：
  - Node：Read `package.json` 的 `scripts`（dev/start/build/test）
  - Python：Read `pyproject.toml` / `requirements.txt`（安装 + 运行命令）
  - 通用：Read `docs/smoke-checks.md`（已有冒烟/单测命令，最可靠）
- 写/更新 `{REPO_DIR}/README.md` 的「快速开始」段：环境要求 + 安装 + 运行 + 测试 + 构建（命令从配置提取）
- **最终用户报告附「怎么运行」一段**（可复制粘贴的命令序列 + 访问地址/端口）

日志：`- {yymmdd hhmm} 📖 运行指南 → README.md（快速开始）`

## Step 3 指标落盘 + 经验提炼（自进化闭环，全能模式）

**Step A — 主Agent 写 metrics.md 结构部分**（从自己的 main-log.md 统计，不读报告内容，不违反上下文规则）：

Grep main-log.md 中 `功能{P/F} / 质量{P/F} / 健壮{P/F} / 安全{P/F} / E2E{P/F}` 形式的行，按维度累计 P/F 计数，写入 `{REPO_DIR}/docs/metrics.md`（覆盖写）：

```markdown
# 质量指标

## 汇总
- 任务总数: {N}
- 平均迭代轮次: {avg}
- 一次通过率: {1次通过数/N}

## 维度失败率
| 维度 | 测试次数 | FAIL 次数 | 失败率 |
|------|---------|----------|--------|
| 功能正确性 | {x} | {y} | {%} |
| 代码质量 | | | |
| 健壮性 | | | |
| 安全性 | | | |
| 端到端 | | | |

## 升级任务
- 3 轮未通过: {N} 个 ({TASK_ID 列表})
```

**Step B — 调用 code-sage 提炼规则（闭环①②③的核心）**：

```
Agent(
  subagent_type: "code-sage",
  prompt: "经验提炼。\n仓库：{REPO_DIR}\n报告目录：{REPO_DIR}/tests/reports/\n指标文件：{REPO_DIR}/docs/metrics.md\n编码规范 skill：coding-standards\n\n请扫描所有测试报告，提炼高频问题标签为防错规则追加到 coding-standards skill；基于 metrics.md 给出失败模式 Top-5 和调优建议追加到 metrics.md 调优段。完成后只返回新增规则数 + 调优建议摘要。"
)
```

日志：`- {yymmdd hhmm} 🧠 经验提炼完成：新增{N}条规则，调优建议{M}条`

**Step B2 — 调优建议路由（sage 建议落地通道）**：

读 `docs/metrics.md`「调优建议」段 → 按每条标注的执行者路由：
- `→ Planner`：契约缺类 → 派 code-planner 补 feature-spec 用例（登记为下版本/新 ⏳）
- `→ PM`：需求模糊 → 记入 prd.md 待确认问题，下轮需求澄清
- `→ Dev`：自查纪律/技术债 → 记入 lessons-learned.md，下一批开发注入 Dev prompt
- `→ 框架维护者`：流程/人设改进 → 记入 main-log.md 收尾报告，随框架版本迭代

日志：`- {yymmdd hhmm} 🧠 调优建议路由：{N} 条已派发`

## Step C 版本归档（时间维度渐进加载——运行时文档只留当前版本）

> **归档机制**：按 `orchestrators/handbook/archive.md` 执行——验收即归档，`feature-spec` / `dev-plan` / `design`（ADR 保留）/ `results.json` / 已消费的旧调研批次剪裁入 `docs/archive/v{version}/`，文件头留**续号锚点**（上次 TASK 编号，新版本从此续号），运行时文件只留当前版本。
> **不归档**：`lessons-learned.md`（经验库）/ `prd.md`（需求池）/ `metrics.md`（指标）/ `env-state.md`（环境当前态）。
> 日志：`- {yymmdd hhmm} 📦 版本归档 → docs/archive/v{version}/（feature-spec/dev-plan/design/results.json/调研批次）`

## Step 4 不退出循环

进入等待状态，检查是否有新需求追加到 `docs/prd.md`。
