# 项目模板契约（Project Template Contract）

> **受众：所有角色**（Planner / Dev / Tester / Ops）。
> 本文件定义项目模板的引用规则、模板内容与业务代码的边界、各角色的模板职责。
>
> **核心原则**：模板提供标准结构，不替代业务设计；模板生成的文件不测，只测业务代码。

---

## 1. 模板目录结构

```
skills/project-templates/
├── ddd/                     # DDD 四层目录模板
│   ├── python-ddd/         # Python DDD 模板
│   ├── node-ddd/           # Node.js DDD 模板
│   ├── go-ddd/             # Go DDD 模板
│   └── java-ddd/           # Java DDD 模板
├── harmonyos/              # 鸿蒙官方模板
├── react/                  # React 模板（预留）
├── vue/                    # Vue 模板（预留）
└── template-contract.md    # 本文件
```

---

## 2. 模板引用方式（Planner 触发）

**主 Agent 调用 Planner 时注入模板参数**：
- `模板：DDD经典结构-Python` → 使用 `python-ddd/`
- `模板：DDD经典结构-Node` → 使用 `node-ddd/`
- `模板：DDD经典结构-Go` → 使用 `go-ddd/`
- `模板：DDD经典结构-Java` → 使用 `java-ddd/`
- `模板：鸿蒙官方` → 使用 `harmonyos/`

**无模板参数时**：Planner 按原逻辑创建基础骨架（`src/`、`tests/`）。

---

## 3. DDD 模板结构（四层目录）

每个 DDD 模板包含以下标准结构：

```
{template}/
├── src/
│   ├── domain/          # 领域层（实体/值对象/聚合/仓储接口/领域服务）
│   │   ├── entities/    # 实体
│   │   ├── value_objects/  # 值对象
│   │   ├── aggregates/  # 聚合根
│   │   ├── repositories/   # 仓储接口
│   │   └── services/   # 领域服务
│   ├── application/     # 应用层（用例编排/应用服务）
│   │   ├── use_cases/  # 用例
│   │   └── services/   # 应用服务
│   ├── interface/       # 接口层（API/CLI/控制器/路由）
│   │   ├── api/        # API 控制器
│   │   └── cli/        # CLI 命令
│   └── infrastructure/  # 基础设施层（仓储实现/DB/外部客户端）
│       ├── persistence/   # 持久化实现
│       ├── external/      # 外部服务客户端
│       └── config/        # 配置
├── tests/
│   ├── unit/            # 单元测试
│   └── integration/     # 集成测试
└── README.md            # 模板说明（标注哪些是模板生成、哪些需业务实现）
```

---

## 4. 角色职责契约

| 角色 | 模板职责 | 约束 |
|------|---------|------|
| **Planner** | 按模板参数创建项目骨架 | ① 选择模板 → ② 复制到项目根 → ③ 在 dev-plan.md 记录"使用模板：{模板名}" |
| **Dev** | 按模板结构开发业务代码 | ① 不删除模板生成的文件（除非 README 明确标注可删除）② 按四层职责分层写码（不跨层调用）③ 模板示例代码仅供参考，不直接复制 |
| **Tester** | 区分模板文件与业务代码 | ① 模板生成的文件不测（如 README/示例代码/配置）② 只测业务代码（dev-plan.md 记录的任务） |
| **Ops** | 按模板约定准备测试环境 | ① 读取模板的 README/配置了解依赖约定② 按模板的端口/数据库规划准备环境 |

---

## 5. 模板文件与业务代码边界

**模板生成文件**（不测、不删、按需修改配置）：
- 目录结构（`src/domain/`、`src/application/` 等）
- 配置文件（`package.json`、`requirements.txt`、`go.mod` 等）
- 示例代码（`README.md` 中的示例、`examples/` 目录）
- 构建脚本（`Makefile`、`build.sh` 等）

**业务代码文件**（需测试、需实现）：
- `src/domain/entities/` 下的实体定义（业务实体）
- `src/application/use_cases/` 下的用例实现（业务逻辑）
- `src/interface/` 下的控制器/路由（业务接口）
- `src/infrastructure/persistence/` 下的仓储实现（数据访问）
- `tests/unit/` 下的单元测试

**判定标准**：
- 文件在模板 README 中标注为"需业务实现" → 业务代码
- 文件是模板自带的示例/配置 → 模板文件
- 不确定时，优先咨询 Planner

---

## 6. 新增模板流程

**框架维护者添加新模板时**：
1. 在 `skills/project-templates/` 下创建新目录
2. 按模板类型组织结构（DDD/官方模板/自定义）
3. 编写 `README.md` 标注：
   - 模板来源（官方/自研）
   - 哪些文件是模板生成的
   - 哪些文件需业务实现
   - 依赖/端口/数据库约定
4. 更新本文件的「模板目录结构」和「模板引用方式」段
5. 同步更新 Planner 人设的模板引用逻辑

---

## 7. 模板测试

**验证模板正确性**：
1. 创建测试项目，调用 Planner 指定模板
2. 检查项目骨架是否符合模板结构
3. Dev 按模板实现一个简单用例
4. Tester 验证是否正确区分模板文件与业务代码

**测试命令**：
```bash
# 在框架目录下执行（需补充测试用例）
cd .claude
# TODO: 补充模板测试用例
```

---

> **维护规则**：新增模板时同步更新本文件 + Planner 人设 + SKILL.md 导航。
