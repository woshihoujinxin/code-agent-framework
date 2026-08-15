# Go DDD 四层目录模板

> **模板来源**：DDD 经典结构适配 Go
> **适用场景**：标准 DDD + 业务规则复杂的项目

---

## 目录结构

```
src/
├── domain/              # 领域层（零外部依赖）
│   ├── entity/          # 实体（有唯一标识与生命周期）
│   ├── valueobject/     # 值对象（无标识、不可变）
│   ├── aggregate/       # 聚合根（外部访问唯一入口）
│   ├── repository/      # 仓储接口（接口定义）
│   └── service/         # 领域服务（跨聚合业务操作）
├── application/         # 应用层（用例编排）
│   ├── usecase/        # 用例（应用服务）
│   └── service/        # 应用服务（协调多个用例）
├── interface/           # 接口层（API/CLI）
│   ├── api/            # API 控制器（Gin/Echo）
│   │   └── handler/    # HTTP 处理器
│   └── cli/            # CLI 命令（Cobra）
└── infrastructure/      # 基础设施层（仓储实现）
    ├── persistence/     # 数据库实现（GORM/sqlx）
    ├── external/        # 外部服务客户端
    └── config/          # 配置（viper）

tests/
├── unit/               # 单元测试（testify/mock）
│   ├── domain/         # 领域层测试
│   ├── application/    # 应用层测试
│   └── interface/      # 接口层测试
└── integration/        # 集成测试（docker-compose）
    └── __test__.go
```

---

## 依赖约定

- **运行时**：Go >= 1.21
- **Web 框架**：Gin（推荐）或 Echo
- **ORM**：GORM（推荐）或 sqlx
- **CLI**：Cobra
- **测试**：标准库 + testify
- **配置**：viper
- **日志**：zap（推荐）或 logrus

---

## 端口与数据库约定

- **开发端口**：8080（后端）
- **测试端口**：8090
- **开发数据库**：`{project}_dev`
- **测试数据库**：`{project}_test`

---

## 模板文件 vs 业务代码

**模板生成文件**（不测、不删）：
- `go.mod`、`go.sum`
- `tests/` 目录结构
- 本 `README.md` 文件

**需业务实现文件**（需测试、需实现）：
- `src/domain/entity/*.go`
- `src/domain/valueobject/*.go`
- `src/domain/aggregate/*.go`
- `src/domain/repository/*.go`
- `src/domain/service/*.go`
- `src/application/usecase/*.go`
- `src/interface/api/handler/*.go`
- `src/infrastructure/persistence/*.go`

---

## 实现示例（参考）

### 1. 实体示例（domain/entity/user.go）

```go
package entity

import (
    "github.com/google/uuid"
)

type User struct {
    ID    uuid.UUID
    Name  string
    Email string
}

func NewUser(name, email string) (*User, error) {
    return &User{
        ID:    uuid.New(),
        Name:  name,
        Email: email,
    }, nil
}
```

### 2. 仓储接口示例（domain/repository/user_repository.go）

```go
package repository

import (
    "context"
    "github.com/google/uuid"
    "src/domain/entity"
)

type UserRepository interface {
    Save(ctx context.Context, user *entity.User) error
    FindByID(ctx context.Context, id uuid.UUID) (*entity.User, error)
}
```

### 3. 用例示例（application/usecase/create_user.go）

```go
package usecase

import (
    "context"
    "src/domain/entity"
    "src/domain/repository"
)

type CreateUserUseCase struct {
    userRepo repository.UserRepository
}

func NewCreateUserUseCase(userRepo repository.UserRepository) *CreateUserUseCase {
    return &CreateUserUseCase{userRepo: userRepo}
}

func (uc *CreateUserUseCase) Execute(ctx context.Context, name, email string) (*entity.User, error) {
    user, err := entity.NewUser(name, email)
    if err != nil {
        return nil, err
    }
    err = uc.userRepo.Save(ctx, user)
    return user, err
}
```

---

## 注意事项

1. **依赖方向**：interface → application → domain（外层指向内层）
2. **domain 层零外部依赖**：不引用任何 framework/database/library（除标准库）
3. **跨聚合修改**：经应用服务协调，不直接穿透对象图
4. **实体行为**：状态变化通过构造函数/方法表达（不暴露 setter）
5. **接口命名**：Go 惯例，接口以 `er` 结尾或描述行为

---

> **维护**：框架维护者 | **最后更新**：2025-08-15
