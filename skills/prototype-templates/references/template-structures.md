# 原型模板标准结构定义

每种模板定义了必需的 HTML 区块、建议的布局方式和内容规范。

---

## 1. web-prototype（通用网页原型）

```html
<!-- 标准结构 -->
<header>
  <!-- Navigation: Logo + Nav links + CTA button -->
</header>

<main>
  <section class="hero">
    <!-- Hero: 大标题 + 副标题 + CTA + Hero image/illustration -->
  </section>

  <section class="features">
    <!-- Features: 3-4 个特性卡片（图标 + 标题 + 描述） -->
  </section>

  <section class="social-proof">
    <!-- Social Proof: Logo 墙 / 数据统计 / 用户评价 -->
  </section>

  <section class="cta-section">
    <!-- Final CTA: 呼唤行动 + 按钮 -->
  </section>
</main>

<footer>
  <!-- Footer: 链接列表 + Copyright -->
</footer>
```

**布局规范**：
- 容器最大宽度：1200px
- Hero 区高度：80-100vh
- Feature 卡片：3-4 列等宽
- 留白：section 间 80-120px

---

## 2. saas-landing（SaaS 落地页）

```html
<header><!-- Sticky nav --></header>

<section class="hero">
  <!-- Product hero: 大标题 + 简述 + 双 CTA（主/次） + 产品截图 -->
</section>

<section class="logos">
  <!-- Trust: "Trusted by" + 公司 logo 行 -->
</section>

<section class="features">
  <!-- 3 核心特性：左右交替布局（文字+截图） -->
</section>

<section class="how-it-works">
  <!-- 步骤式说明：1-2-3 步流程 -->
</section>

<section class="testimonials">
  <!-- 用户评价：2-3 条真实感评价卡片 -->
</section>

<section class="pricing">
  <!-- 定价方案：2-3 列（推荐方案高亮） -->
</section>

<section class="faq">
  <!-- FAQ: 手风琴式展开 -->
</section>

<section class="final-cta">
  <!-- 最终 CTA: 简洁有力的行动呼唤 -->
</section>

<footer><!-- 完整 footer --></footer>
```

---

## 3. dashboard（数据仪表盘）

```html
<div class="layout">
  <aside class="sidebar">
    <!-- Sidebar: Logo + Nav menu + User info -->
  </aside>

  <main class="content">
    <header class="topbar">
      <!-- Top bar: 页面标题 + 搜索 + 通知 + 用户头像 -->
    </header>

    <section class="stats">
      <!-- KPI 卡片行：4 个关键指标卡片 -->
    </section>

    <section class="charts">
      <!-- 图表区：1-2 个大图表（线图/柱图） -->
    </section>

    <section class="table">
      <!-- 数据表格：可排序列表 -->
    </section>
  </main>
</div>
```

**布局规范**：
- Sidebar 宽度：240px（可折叠到 64px）
- 内容区填充：24px
- KPI 卡片：4 列等宽
- 信息密度：高（紧凑间距）

---

## 4. mobile-app（移动端 App）

```html
<div class="device-frame iphone-15-pro">
  <div class="screen">
    <header class="status-bar">
      <!-- iOS 状态栏模拟 -->
    </header>

    <nav class="app-header">
      <!-- App header: 标题 + 操作按钮 -->
    </nav>

    <main class="app-content">
      <!-- 主内容区 -->
    </main>

    <nav class="tab-bar">
      <!-- 底部 Tab: 4-5 个图标+文字 -->
    </nav>
  </div>
</div>
```

**布局规范**：
- 设备宽度：375px（iPhone 15 Pro）
- 安全区：top 44px, bottom 34px
- 内容 padding：16px
- 圆角：遵循 iOS/Android 规范

---

## 5. simple-deck（简洁演示）

```html
<div class="deck">
  <section class="slide" data-slide="1">
    <!-- 封面：大标题 + 副标题 + 演讲者信息 -->
  </section>

  <section class="slide" data-slide="2">
    <!-- 议程/目录 -->
  </section>

  <section class="slide" data-slide="3">
    <!-- 内容幻灯片：标题 + 要点列表或图表 -->
  </section>

  <!-- 更多幻灯片... -->

  <nav class="slide-nav">
    <!-- 幻灯片导航：上一页/下一页 + 页码 -->
  </nav>
</div>
```

**布局规范**：
- 幻灯片比例：16:9
- 每屏一个核心信息
- 水平滑动切换

---

## 6. pricing-page（定价页）

```html
<header><!-- Nav --></header>

<section class="pricing-hero">
  <!-- 标题 + 简述 + 年/月切换 -->
</section>

<section class="pricing-cards">
  <!-- 2-3 列定价卡片（推荐方案视觉突出） -->
  <div class="plan"><!-- Starter --></div>
  <div class="plan featured"><!-- Pro（推荐） --></div>
  <div class="plan"><!-- Enterprise --></div>
</section>

<section class="feature-matrix">
  <!-- 特性对比表：功能 × 方案 的矩阵 -->
</section>

<section class="faq">
  <!-- 定价相关 FAQ -->
</section>
```

---

## 7. docs-page（文档页）

```html
<div class="docs-layout">
  <aside class="sidebar-nav">
    <!-- 左侧导航：可折叠的目录树 -->
  </aside>

  <main class="doc-content">
    <!-- 文档正文：标题 + 正文 + 代码块 + 提示框 -->
  </main>

  <aside class="toc">
    <!-- 右侧 TOC：当前页面的标题锚点 -->
  </aside>
</div>
```

**布局规范**：
- 三栏布局：240px + auto + 200px
- 正文最大宽度：720px
- 代码块：深色背景 + 语法高亮

---

## 8. blog-post（博客文章）

```html
<header><!-- 顶部导航 --></header>

<article class="post">
  <header class="post-header">
    <!-- 文章标题 + 作者 + 日期 + 标签 -->
  </header>

  <figure class="cover">
    <!-- 封面图 -->
  </figure>

  <div class="post-body">
    <!-- 正文内容：段落 + 引用 + 图片 + 代码块 -->
  </div>

  <footer class="post-footer">
    <!-- 作者简介 + 分享按钮 + 相关文章 -->
  </footer>
</article>
```

**布局规范**：
- 正文最大宽度：680px
- 段落字号：18px，行高 1.7
- 标题使用衬线或半衬线字体

---

## 9. email-template（邮件模板）

```html
<!-- 邮件用 table 布局确保兼容性 -->
<table class="email-wrapper" width="600" cellpadding="0" cellspacing="0">
  <tr>
    <td class="email-header">
      <!-- Logo + 预览文本 -->
    </td>
  </tr>
  <tr>
    <td class="email-hero">
      <!-- Hero 图片 + 标题 -->
    </td>
  </tr>
  <tr>
    <td class="email-body">
      <!-- 正文内容 -->
    </td>
  </tr>
  <tr>
    <td class="email-cta">
      <!-- CTA 按钮（用 table 实现 bulletproof button） -->
    </td>
  </tr>
  <tr>
    <td class="email-footer">
      <!-- 退订链接 + 联系方式 -->
    </td>
  </tr>
</table>
```

**布局规范**：
- 总宽度：600px
- 使用 table 布局（非 flexbox/grid）
- 内联 CSS（不依赖 <style>）
- 图片需要 alt 和 width 属性

---

## 10. cli-prototype（交互式 CLI / TUI——Agent/终端产品）

> CLI/TUI 无 HTML 界面，原型是**交互设计文档**（命令树 + --help + 交互流程 + 终端样式 + 示例会话），作为 CLI 实现的 UX 基准。产出：`cli.md` + `DESIGN.md` + `README.md`。

### cli.md 结构

```markdown
# {工具名} CLI 原型

## 1. 命令树
{命令层级：`{name} <subcommand> [flags] [args]`，含每个命令一句话用途}

## 2. --help 输出（真实排版）
{格式化 help：用法 / 参数表 / 子命令 / 示例，等宽排版}

## 3. 核心交互流程（提示符对话 / TUI 屏）
{每个关键交互一屏：提示符 + 输入 + 输出（含错误分支）}

## 4. 错误与边界
{错误提示样式、未知命令、参数校验失败、中断恢复}

## 5. 示例终端会话
{一段完整 mock 会话，展示典型使用路径}
```

### DESIGN.md（CLI 设计令牌）

- **命令命名**：动词开头 + kebab-case（`run`/`delegate`/`export-doc`）；子命令层级一致
- **提示符**：`❯` / `$` / `{产品名}>`（交互式）；非交互命令无提示符
- **输出格式**：行宽 ≤80；表格等宽对齐；关键信息（成功/错误/高亮）用有限颜色
- **ANSI 配色**：终端安全色（默认白/青/绿/黄/红），禁全彩渐变、禁花哨动画
- **交互模式**：prompt 确认 / 进度指示 / 中断（Ctrl-C）恢复
- **错误规范**：`✖ 错误：{原因} → {修复建议}`（不裸抛堆栈）

### Anti-Slop（CLI 版）

- ❌ emoji 当图标滥用、ANSI 彩虹/动画、装饰性 ASCII 框堆叠、命令命名不一致
- ✅ 帮助自解释（不用看文档）、输出一致、错误可恢复、真实占位

---

## 通用内容规范

- **使用真实感的占位内容**，不用 Lorem ipsum
- **数据用占位符**：`—` 或 `[TBD]`，不编造
- **按钮用行动动词**："开始免费试用"、"查看方案"，不用"了解更多"、"点击这里"
- **图片用内联 SVG**：几何图形占位，不依赖外部资源
