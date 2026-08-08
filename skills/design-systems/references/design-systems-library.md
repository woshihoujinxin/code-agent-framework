# 精选 12 套设计系统令牌库

紧凑令牌，每套 ~20 行：特征 / 调色板 / 字体 / 组件签名 / Cautions。选型时优先匹配 PRD「视觉意图」段的场景与调性；拿不准用 `Default` 兜底。

> 色值为公开品牌风格的参考，按项目微调时保持品牌气质。

---

## 1. Claude（AI 产品）
- **特征**：温暖、克制的"人文科技"感；暖陶土橙 + 米白，圆润友好不花哨
- **Primary**: `#D97757`（暖陶土橙）· hover `#B86547`
- **Neutral**: bg `#FDFDFC` / surface `#F5F4F1` / border `#E8E6E1` / text `#191919` / muted `#73736E`
- **Font**: Sans（系统 + Inter fallback）；标题与正文同字体，靠字重分级
- **组件**：圆角 `12px`；主按钮 = 陶土橙底 + 深色字；卡片无阴影、极细边框
- **Cautions**：禁荧光色；禁玻璃拟态；禁过多圆角堆叠
- **Agent 提示**：留白大方，文案克制，暖色点缀只用于 CTA 与高亮

## 2. Linear（开发者工具，暗色旗舰）
- **特征**：精密、数据感、深紫极简；信息密度高但呼吸感好
- **Primary**: `#5E6AD2`（线性紫）· hover `#7C87E8`
- **Neutral（暗色）**: bg `#08090A` / surface `#17181C` / border `#26272C` / text `#FBFCFC` / muted `#8A8F98`
- **Font**: 几何无衬线（Inter）；`mono` 用于数据
- **组件**：圆角 `6px`；按钮暗底 + 细边框；卡片表面色 + 1px 边框，无重阴影
- **Cautions**：禁彩虹渐变；禁 emoji 图标；禁过度发光
- **Agent 提示**：深色为主，紫只作强调；数据表紧凑右对齐；状态用语义色

## 3. Vercel（开发者工具，黑白旗舰）
- **特征**：黑白单色、超高对比、几何无衬线；唯一强调色来自内容
- **Primary**: `#000000`（黑）· 强调用白/透明，极少彩色
- **Neutral**: bg `#FFFFFF` / surface `#FAFAFA` / border `#E5E5E5` / text `#171717` / muted `#737373`
- **Font**: 几何无衬线（Geist / Inter fallback）
- **组件**：圆角 `6px`；按钮黑底白字；卡片 1px 边框；阴影极浅
- **Cautions**：禁彩色渐变；禁花哨图标；禁止同页超 2 种主色
- **Agent 提示**：纯黑白灰三层，用字号/字重/留白建立层级，而不是颜色

## 4. Notion（生产力/文档）
- **特征**：素净、内容优先、无框架感；衬线标题 + 无衬线正文
- **Primary**: `#2383E2`（Notion 蓝）· 弱化使用时 `#37352F`（文本墨色）
- **Neutral**: bg `#FFFFFF` / surface `#F7F6F3` / border `#E9E9E7` / text `#37352F` / muted `#8B8B8B`
- **Font**: 标题衬线（Georgia / Noto Serif fallback），正文无衬线（系统栈）
- **组件**：圆角 `8px`；按钮次强调；卡片纯表面色无边框；大量留白
- **Cautions**：禁高饱和色块；禁强阴影；禁过度装饰
- **Agent 提示**：内容密度随意但间距一致；标题用衬线制造"文档感"

## 5. Raycast（效率工具）
- **特征**：清爽、直给、命令式 UI；红强调色醒目但不躁
- **Primary**: `#FF6363`（珊瑚红）· hover `#FF8181`
- **Neutral**: bg `#FFFFFF` / surface `#F6F6F6` / border `#E5E5E5` / text `#171718` / muted `#8E8E93`
- **Font**: 无衬线（系统栈 + Inter）；等宽用于命令
- **组件**：圆角 `8px`；输入框显著（搜索即中心）；列表行 hover 变色
- **Cautions**：禁 emoji 图标（用线性 SVG）；禁 4+ 色；禁装饰性动画
- **Agent 提示**：布局以"一个搜索/输入焦点"为核心，其余极简

## 6. Supabase（开发者工具）
- **特征**：深色 + 明亮绿强调，"开源/数据"气质，现代但不过度
- **Primary**: `#3ECF8E`（Supabase 绿）· hover `#33B981`
- **Neutral（暗色可选）**: bg `#1F1E24` / surface `#2A2932` / border `#3E3D4A` / text `#EAE9F0` / muted `#9B9AAD`
- **Font**: 无衬线（Inter / 系统栈）；代码 `mono`
- **组件**：圆角 `8px`；主按钮绿底深字；卡片表面色 + 细边框
- **Cautions**：禁紫渐变；禁圆形图标乱入；禁无对比度的浅绿文字
- **Agent 提示**：绿色只用于主要操作与品牌强调，数据区保持中性

## 7. Stripe（金融科技）
- **特征**：清新、信任、极简金融感；靛紫主色 + 大量留白
- **Primary**: `#635BFF`（Stripe 靛紫）· hover `#5851EC`
- **Neutral**: bg `#FFFFFF` / surface `#F6F8FA` / border `#E3E8EE` / text `#0A2540`（深海军蓝）/ muted `#425466`
- **Font**: 几何无衬线（Inter / 系统栈）
- **组件**：圆角 `10px`；主按钮靛紫底白字；卡片表面色；阴影柔和
- **Cautions**：禁彩虹渐变；禁 emoji 图标；禁营销感过重的色块
- **Agent 提示**：金融感靠"清晰 + 可信"而非装饰；数字用 tabular-nums

## 8. Apple（消费电子）
- **特征**：极致简洁、留白大师、无边框层级；靠内容自身建立层次
- **Primary**: `#0071E3`（Apple 蓝，仅链接/按钮少量使用）
- **Neutral**: bg `#FFFFFF` / surface `#F5F5F7` / border `#D2D2D7` / text `#1D1D1F` / muted `#6E6E73`
- **Font**: SF 系（-apple-system 栈）；超大字重标题
- **组件**：圆角 `12px`（按钮 pill 可选）；几乎无边框，靠卡片表面色；阴影极轻
- **Cautions**：禁 4+ 色；禁强边框；禁阴影堆叠；禁小字挤占
- **Agent 提示**：大字号、大留白、少元素；一张图一句话一个 CTA

## 9. Shopify（电商/消费）
- **特征**：友好、可信、活泼但克制；品牌绿 + 暖中性色
- **Primary**: `#96BF48`（Shopify 绿）· 深色文本 `#212326`
- **Neutral**: bg `#FFFFFF` / surface `#F5F6F7` / border `#D9DDE1` / text `#212326` / muted `#6F7377`
- **Font**: 无衬线（系统栈 + Inter）
- **组件**：圆角 `8px`；主按钮绿底白字；卡片 1px 边框
- **Cautions**：禁荧光绿文字；禁 emoji 图标；禁同页多强调色
- **Agent 提示**：电商感靠"清晰的购买路径 + 信任元素"，别堆促销色

## 10. Spotify（媒体/消费）
- **特征**：暗色沉浸 + 品牌绿强调；圆润、动感、音乐气质
- **Primary**: `#1DB954`（Spotify 绿）· hover `#1ED760`
- **Neutral（暗色）**: bg `#121212` / surface `#1F1F1F` / border `#2A2A2A` / text `#FFFFFF` / muted `#B3B3B3`
- **Font**: 圆润无衬线（Circular / system fallback）；标题粗
- **组件**：圆角 `8px`（pill 按钮）；卡片表面色 + hover 亮起；绿只用于播放/CTA
- **Cautions**：禁彩虹渐变；禁 emoji 图标；禁过量动效（可 reduced-motion）
- **Agent 提示**：暗底 + 白字 + 绿色强调三件套；卡片 hover 是主要反馈

## 11. Default（Neutral Modern，通用兜底）
- **特征**：安全、中性、任何场景不犯错；蓝强调 + 灰中性
- **Primary**: `#0066FF` / hover `#0052CC`
- **Neutral**: bg `#FFFFFF` / surface `#F8F9FA` / border `#E2E8F0` / text `#1A202C` / muted `#64748B`
- **Font**: 无衬线（Inter / 系统栈）
- **组件**：圆角 `8px`；主按钮主色底白字；卡片表面色 + 1px 边框 + 极浅阴影
- **Cautions**：禁紫渐变；禁 4+ 色；禁 emoji 图标；禁编造数据
- **Agent 提示**：这是最后兜底，优先从上方 10 套品牌里选

## 12. Warm Editorial（暖编辑，通用起始）
- **特征**：暖调、编辑感、内容型；衬线 + 暖中性色
- **Primary**: `#B45309`（暖琥珀）· 文本深棕 `#292524`
- **Neutral**: bg `#FDFCFA` / surface `#F7F5F0` / border `#E8E3DA` / text `#292524` / muted `#78716C`
- **Font**: 标题衬线（Georgia / Noto Serif），正文无衬线
- **组件**：圆角 `6px`；按钮琥珀底；卡片细边框 + 无阴影
- **Cautions**：禁冷色高饱和块；禁 emoji 图标；禁过度圆角
- **Agent 提示**：适合博客/文档/品牌故事页；暖白底 + 衬线标题 + 琥珀点缀
