# 渲染呈现验证（UI / CLI / TUI）

> **受众**：`code-tester-e2e`（执行渲染验证）+ `code-dev-frontend`（开发前知道怎么验）。
> **何时读**：e2e 测试前端 Web / CLI / TUI 任务时，按项目类型读对应段。纯算法/无界面任务跳过。
> **定位**：这是**动态呈现验证**（实际跑出来看）。静态查源码的视觉防错（Anti-Slop）归 quality，本文件专管"实际呈现对不对"。

## 核心原则

用户最关心"看着对、用得了、用着顺"——这些在使用时才暴露的问题，测试要**间接等价**兜住：
- **确定性断言打底**（数值/结构/可达，100% 准）
- **视觉模型补充**（整体观感，有偏差但能抓大问题）

---

## 一、Web 前端任务

### 1. 启动 + 截图（Playwright 无头）

```bash
# 截图（全页 + 关键视口）
npx playwright screenshot --viewport-size=1440,900 --full-page http://localhost:5173 page-desktop.png
npx playwright screenshot --viewport-size=375,667 http://localhost:5173 page-mobile.png
```
前端 Dev 须在交付前起好本地服务（端口见 design.md「端口与库规划」），e2e 连该端口截图。

### 2. computed style 数值断言（确定性，不靠眼睛）

提取实际元素样式，**数值对比 `docs/prototype/DESIGN.md` 令牌**：
```js
// Playwright 取 computed style
const color = await page.locator('.btn-primary').evaluate(el => getComputedStyle(el).backgroundColor);
// 断言 = DESIGN.md 的 primary token（如 rgb(59,130,246) = #3B82F6）
```
查：主色/字体族/字号/圆角/间距 是否落在 DESIGN.md token 上（允许合理落地差异，偏离注明）。

### 3. 视觉模型对比原型（整体观感）

实现截图 + 原型 `docs/prototype/index.html` 截图，一起发视觉模型（`analyze_image`）：
> "对比这两张图，实现是否偏离原型？颜色/字体/布局/留白一致吗？有无明显错位、溢出、重叠？"

### 4. DOM 结构 diff（结构偏离）

实现 DOM 标签树 vs 原型 DOM——结构差异（缺语义标签、布局容器错位）= 偏离点。

### 5. 交互可达性（用得了）

Playwright 跑核心用户流（点击→跳转→表单→提交），断言：元素可见/可点/状态变化。所有交互元素（button/a/input）存在且可聚焦。

---

## 二、CLI 任务（命令行输出）

> **优势**：输出是文本，可逐字精确断言——比 Web 视觉好测。e2e 的"验证输出"已覆盖核心（①②③），本段是增强参考。

### 核心断言（e2e 已做）
- ① 命令退出码（0 成功 / 1 业务错 / 2 参数错）
- ② stdout 精确文本/格式（正则或全量匹配）
- ③ stderr 清晰错误文案

### 增强断言（本段补）
- **④ ANSI 颜色/样式**：解析输出 ANSI 码，断言该有的颜色/加粗在、颜色值对（不靠眼看，靠码）
- **⑤ 表格对齐**：列宽/对齐校验（多行输出列对齐，不串行）
- **⑥ --help 完整性**：所有子命令都在、用法清晰、无遗漏
- **⑦ 管道/重定向兼容**：`todo list | grep X` / `todo add Y > file` 不挂（很多 CLI 在这崩）

### 对比原型
`--help` 输出 + 命令输出格式 vs `docs/prototype/cli.md` 描述——偏离即不一致。

---

## 三、TUI 任务（全屏终端 UI）

> **核心武器**：`tmux capture-pane` 把全屏 UI 转成可断言的文本矩阵；`pexpect` 模拟按键。这俩是 TUI 的 Playwright。

### 1. tmux 抓屏断言（布局/内容）

```bash
tmux new-session -d -s tui "python -m app"   # 后台跑 TUI
sleep 1
tmux capture-pane -t tui -p > screen.txt     # 抓屏幕文本矩阵
# 断言：标题在第1行 / 列表项在第3-10行 / 输入框在底部 / 提示符正确
```
全屏布局的**文本快照**——位置/内容都可精确断言（不像像素有歧义）。

### 2. pexpect 模拟按键（交互可达）

```python
import pexpect
p = pexpect.spawn("python -m app")
p.sendline("input")          # 模拟输入
p.sendcontrol("j")           # Enter
p.expect("预期响应文本")      # 断言每步状态
# ↓↑选择、Tab切焦点、q退出——每步 expect 状态变化
```
验证：焦点移动/选中项高亮/弹窗出现/流程可完成。

### 3. 渲染图 → 视觉模型（整体观感）

抓屏输出（含 ANSI）用 `aha`（ANSI→HTML）或 `ansilove`（→PNG）渲染成图，发 `analyze_image` 评：布局乱不乱、颜色刺不刺眼、对齐错没错、响应式断裂。

### 4. 对比原型 mock-cli

原型 `docs/prototype/mock-cli.{py|ts}` 是**可运行模拟器**：
- 跑 mock-cli 抓屏 vs 跑实现抓屏
- diff 两个屏幕矩阵 → 偏离点（实现和原型布局/交互不一致处）

---

## 按项目类型触发（e2e 选段）

| 项目类型 | 走本文件哪段 | 主要工具 |
|---------|------------|---------|
| Web 前端 | 一、Web | Playwright + analyze_image + DESIGN.md |
| 纯 CLI | 二、CLI（①②③已做，补④⑤⑥⑦）| ANSI 解析 + --help + 管道 |
| TUI | 三、TUI | tmux capture-pane + pexpect + mock-cli |
| 纯算法/无界面 | 跳过 | — |

## FAIL 判定（供 e2e 写报告）

- `E-VISUAL-MISMATCH`：实际呈现偏离原型/DESIGN.md 令牌（颜色/字体/布局错位），或视觉模型判严重偏离
- `E-LAYOUT-BROKEN`：元素溢出/重叠/不可见/不可点（确定性断言失败）
- 交互不可达（Playwright/pexpect 跑不通核心流）→ 归 `E-CMD-FAIL`（已有）
