# 模板系统测试（Template System Tests）

> **测试目标**：验证 Planner 能否正确引用模板生成项目骨架
> **测试方式**：通过提示词直接调用 Planner，验证生成的项目结构

---

## 测试用例

| 用例ID | 模板参数 | 预期项目结构 | 提示词文件 |
|--------|---------|-------------|-----------|
| TC-001 | 模板：DDD经典结构-Java | src/{domain,application,interface,infrastructure}/ | prompts/java-ddd.md |
| TC-002 | 模板：鸿蒙官方 | AppScope/, entry/, oh-package.json5 | prompts/harmonyos.md |
| TC-003 | 无模板 + 方法论：DDD | src/{domain,application,interface,infrastructure}/ | prompts/ddd-no-template.md |
| TC-004 | 无模板 + 无DDD | src/ | prompts/default-skeleton.md |

---

## 测试执行

```bash
# 执行单个测试
./run-test.sh TC-001

# 执行所有测试
./run-all-tests.sh
```

---

## 验证标准

| 验证项 | 标准 |
|--------|------|
| 目录创建 | 模板目录结构完整 |
| dev-plan.md | "使用模板"字段正确记录 |
| README.md | 模板说明文件存在 |
| 依赖约定 | 端口/数据库配置符合模板 |

---

## 测试报告

测试结果记录在 `reports/` 目录：
- `{TC-XXX}-report.txt`：执行结果
- `summary.txt`：汇总报告
