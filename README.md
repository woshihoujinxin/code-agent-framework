# 无人值守多智能体编码框架

一套基于 Claude Code 的多智能体编码系统：**提需求 → 自动开发 → 持续迭代，越用越聪明**。

PM → 架构师（生成测试契约）→ 前后端开发（写单测+自检）→ 五维测试（功能/质量/健壮/安全/E2E）→ 修正循环 → code-sage 提炼规则。三层闭环：批次循环 / 修正循环 / 自进化循环。

## 一句话用

在你的项目里 clone 到 `.claude/`：
```bash
cd my-project
git clone https://github.com/woshihoujinxin/<repo>.git .claude
```
重启 Claude Code（加载新 agents/commands），然后：
```
/dev 用 Python 做个 Todo CLI，支持增删改查    # 高质量代码（五维质量门）
/ship 做个 API 服务并打包成 Docker 镜像        # 可部署制品（审查→构建→校验）
```

> 若不希望 `.claude/` 带嵌套 `.git`：`git clone ... .claude && rm -rf .claude/.git`

## 包含

| 目录 | 内容 |
|------|------|
| `agents/` | 13 个 subagent（PM / 架构师 / 前后端 Dev / 五维 Tester / code-sage） |
| `commands/` | `/dev`（研发质量编排）、`/ship`（交付编排）入口 |
| `orchestrators/` | 两个编排器定义 + 完整文档 + demo |
| `skills/coding-standards/` | 编码规范 + 自进化规则库（code-sage 自动追加） |

## 文档

详细架构、**三层流转图**、角色职责、测试契约机制、自进化闭环——见 [`orchestrators/README.md`](./orchestrators/README.md)。
