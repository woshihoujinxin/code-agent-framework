# Node.js DDD 四层目录模板

> **模板来源**：DDD 经典结构适配 Node.js（TypeScript）
> **适用场景**：标准 DDD + 业务规则复杂的项目

---

## 目录结构

```
src/
├── domain/              # 领域层（零外部依赖）
│   ├── entities/        # 实体（有唯一标识与生命周期）
│   ├── value-objects/   # 值对象（无标识、不可变）
│   ├── aggregates/      # 聚合根（外部访问唯一入口）
│   ├── repositories/    # 仓储接口（接口定义）
│   └── services/        # 领域服务（跨聚合业务操作）
├── application/         # 应用层（用例编排）
│   ├── use-cases/      # 用例（应用服务）
│   └── services/        # 应用服务（协调多个用例）
├── interface/           # 接口层（API/CLI）
│   ├── api/            # API 控制器（Express/Fastify）
│   │   ├── controllers/ # 控制器
│   │   └── routes/      # 路由定义
│   └── cli/            # CLI 命令（Commander/Yargs）
└── infrastructure/      # 基础设施层（仓储实现）
    ├── persistence/     # 数据库实现（Prisma/Mongoose）
    ├── external/        # 外部服务客户端（axios/got）
    └── config/          # 配置（dotenv/config）

tests/
├── unit/               # 单元测试（jest + mock）
│   ├── domain/         # 领域层测试
│   ├── application/    # 应用层测试
│   └── interface/      # 接口层测试
└── integration/        # 集成测试（supertest）
    └── __test__.ts
```

---

## 依赖约定

- **运行时**：Node.js >= 18
- **语言**：TypeScript >= 5
- **Web 框架**：Express（推荐）或 Fastify
- **ORM**：Prisma（推荐）或 Mongoose
- **CLI**：Commander 或 Yargs
- **测试**：Jest + ts-jest
- **依赖注入**：inversify（推荐）或 tsyringe

---

## 端口与数据库约定

- **开发端口**：3000（后端）/ 5173（前端）
- **测试端口**：3001（后端）/ 5184（前端）
- **开发数据库**：`{project}_dev`
- **测试数据库**：`{project}_test`

---

## 模板文件 vs 业务代码

**模板生成文件**（不测、不删）：
- `package.json`、`tsconfig.json`
- `tests/` 目录结构
- 本 `README.md` 文件

**需业务实现文件**（需测试、需实现）：
- `src/domain/entities/*.ts`
- `src/domain/value-objects/*.ts`
- `src/domain/aggregates/*.ts`
- `src/domain/repositories/*.ts`
- `src/domain/services/*.ts`
- `src/application/use-cases/*.ts`
- `src/interface/api/controllers/*.ts`
- `src/interface/api/routes/*.ts`
- `src/infrastructure/persistence/*.ts`

---

## 实现示例（参考）

### 1. 实体示例（domain/entities/User.ts）

```typescript
export class User {
  constructor(
    public readonly id: string,
    public name: string,
    private email: string
  ) {}

  static create(name: string, email: string): User {
    return new User(crypto.randomUUID(), name, email);
  }

  getEmail(): string {
    return this.email;
  }
}
```

### 2. 仓储接口示例（domain/repositories/IUserRepository.ts）

```typescript
import { User } from '../entities/User';

export interface IUserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
}
```

### 3. 用例示例（application/use-cases/CreateUserUseCase.ts）

```typescript
import { User } from '../../domain/entities/User';
import { IUserRepository } from '../../domain/repositories/IUserRepository';

export class CreateUserUseCase {
  constructor(private userRepo: IUserRepository) {}

  async execute(name: string, email: string): Promise<User> {
    const user = User.create(name, email);
    await this.userRepo.save(user);
    return user;
  }
}
```

---

## 注意事项

1. **依赖方向**：interface → application → domain（外层指向内层）
2. **domain 层零外部依赖**：不引用任何 framework/database/library
3. **跨聚合修改**：经应用服务协调，不直接穿透对象图
4. **实体行为**：状态变化通过领域方法表达（不暴露 setter 裸改）
5. **类型安全**：充分利用 TypeScript 类型系统

---

> **维护**：框架维护者 | **最后更新**：2025-08-15
