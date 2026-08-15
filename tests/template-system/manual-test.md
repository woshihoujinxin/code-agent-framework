# 模板系统手动测试指南

## 问题说明
`claude -p` 命令在 Git Bash 环境中可能不可用，需要手动测试。

## 手动测试步骤

### TC-001: Java DDD 模板测试

1. **创建测试项目**：
```bash
mkdir -p /tmp/java-ddd-test && cd /tmp/java-ddd-test
```

2. **复制框架**：
```bash
cp -r /c/develop/aiws/.claude .claude
```

3. **在 Claude Code 中执行以下提示词**：
```
你是编码项目架构师。请为以下需求创建开发计划：

需求：做一个用户管理系统

技术要求：
- 模板：DDD经典结构-Java
- 版本号：v0.0.1

请创建项目骨架、dev-plan.md、design.md、feature-spec.md。
```

4. **验证结果**：
```bash
# 检查目录结构
ls -la src/

# 应该看到：
# domain/
# application/
# interface/
# infrastructure/

# 检查 dev-plan.md 模板字段
grep "使用模板" docs/dev-plan.md

# 应该看到：
# 使用模板：DDD经典结构-Java
```

### TC-002: 鸿蒙官方模板测试

同上，但提示词改为：
```
你是编码项目架构师。请为以下需求创建开发计划：

需求：做一个鸿蒙记事本应用

技术要求：
- 模板：鸿蒙官方
- 版本号：v0.0.1

请创建项目骨架、dev-plan.md、design.md、feature-spec.md。
```

验证：
```bash
ls -la AppScope/ entry/
grep "使用模板.*鸿蒙" docs/dev-plan.md
```

---

## 预期结果

| 测试 | 预期目录 | 预期模板字段 |
|------|---------|-------------|
| TC-001 | src/{domain,application,interface,infrastructure}/ | 使用模板：DDD经典结构-Java |
| TC-002 | AppScope/, entry/, oh-package.json5 | 使用模板：鸿蒙官方 |
| TC-003 | src/{domain,application,interface,infrastructure}/ | 使用模板：无模板 |
| TC-004 | src/（无子目录） | 使用模板：无模板 |

---

## 故障排查

如果模板没有正确引用，检查：
1. Planner 人设是否包含模板逻辑
2. 模板文件是否存在（`skills/project-templates/`）
3. 主 Agent 是否正确注入了"模板："参数
