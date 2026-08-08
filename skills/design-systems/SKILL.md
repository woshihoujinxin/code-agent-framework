---
name: design-systems
description: |
  品牌级设计系统知识库：12 套精选系统 + 9 段结构规范 + 5 大视觉方向 + 品牌提取协议。
  前端开发与原型构建据此生成"非 AI 味"的视觉基准。触发词：设计系统、视觉风格、设计令牌、DESIGN.md、配色、字体、原型样式。
---

# 设计系统知识库（design-systems）

品牌级设计系统参考，帮助前端开发与原型构建**站在巨人的肩膀上**做视觉，避免 AI 随机选色导致的平庸结果。

## 组成部分

| 文件 | 内容 |
|------|------|
| `@references/design-system-schema.md` | DESIGN.md 9 段结构规范（色彩/排版/组件/布局/深度/禁区/响应式/Agent指南） |
| `@references/visual-directions.md` | 5 大视觉方向（编辑质感/现代极简/技术工具/粗犷/柔和）+ 需求→方向选择指南 |
| `@references/brand-extraction-protocol.md` | 品牌提取 5 步法（有自有品牌时） |
| `@references/design-systems-library.md` | **精选 12 套设计系统紧凑令牌**（Claude/Linear/Vercel/Notion/Raycast/Supabase/Stripe/Apple/Shopify/Spotify/Default/Warm Editorial） |

## 使用流程

1. **看需求**：读 PRD 的「视觉意图」段（场景/受众/调性/品牌/规模）
2. **定方向**：按 `visual-directions.md` 的"选择指南"从 5 大视觉方向中定位
3. **选系统**：从 `design-systems-library.md` 选 1 套匹配的（默认 `Default (Neutral Modern)` 兜底）
4. **出令牌**：按 `design-system-schema.md` 9 段结构生成项目专属 `DESIGN.md`（色彩 HEX+CSS 变量、字体栈、组件规范）
5. **有品牌**：用户已有品牌 → 执行 `brand-extraction-protocol.md` 5 步提取，品牌色值 + 匹配结构 = 专属令牌

## 输出格式

生成项目专属 `DESIGN.md`，遵循 9 段标准结构；前端实现时以 CSS 变量对齐令牌。

## 注意

- 每套系统末尾的 **Cautions** 是本套的禁区，生成时必须遵守
- 色彩必须过 WCAG AA 对比度（正文 ≥4.5:1，大标题 ≥3:1）；不达标只建议不改
- 令牌中的 HEX 是"参考风格"，按项目微调时保持品牌气质
