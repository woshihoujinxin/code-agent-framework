# 模板系统测试快速指南

## 快速开始

### 单个测试
```bash
cd .claude/tests/template-system
./run-test.sh TC-001
```

### 批量测试
```bash
cd .claude/tests/template-system
./run-all-tests.sh
```

### 手动验证
```bash
cd .claude/tests/template-system
./validation/validate.sh TC-001 /tmp/template-test-TC-001
```

---

## 测试用例说明

| 用例ID | 模板 | 预期结构 | 提示词 |
|--------|------|---------|--------|
| TC-001 | Java DDD | 四层目录 | prompts/java-ddd.md |
| TC-002 | 鸿蒙官方 | AppScope/entry/ | prompts/harmonyos.md |
| TC-003 | DDD 注入 | 四层目录（手工）| prompts/ddd-no-template.md |
| TC-004 | 默认骨架 | src/（基础）| prompts/default-skeleton.md |

---

## 测试原理

1. **提示词触发**：通过 `claude -p` 发送提示词给 Planner
2. **框架复制**：测试项目获得 `.claude/` 目录
3. **Planner 执行**：按模板参数创建项目骨架
4. **结果验证**：检查目录结构、dev-plan.md 字段

---

## 手动测试步骤（无需脚本）

如果你想手动测试：

```bash
# 1. 创建测试项目
mkdir -p /tmp/my-test && cd /tmp/my-test

# 2. 复制框架
cp -r /path/to/.claude .claude

# 3. 发送提示词给 Planner
claude -p "你是编码项目架构师。请为以下需求创建开发计划：需求：做一个用户管理系统。技术要求：模板：DDD经典结构-Java、版本号：v0.0.1。请创建项目骨架、dev-plan.md、design.md、feature-spec.md。"

# 4. 检查结果
ls -la src/
grep "使用模板" docs/dev-plan.md
```

---

## 故障排查

**问题**：claude 命令找不到
- **解决**：检查 Claude Code CLI 是否已安装

**问题**：模板未正确引用
- **解决**：检查 Planner 人设是否包含模板逻辑

**问题**：目录结构不符合预期
- **解决**：检查模板文件是否存在、.gitignore 是否排除
