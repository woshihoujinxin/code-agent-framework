# Python DDD 四层目录模板

> **模板来源**：DDD 经典结构适配 Python
> **适用场景**：标准 DDD + 业务规则复杂的项目

---

## 目录结构

```
src/
├── domain/               # 领域层（零外部依赖）
│   ├── __init__.py
│   ├── entities/        # 实体（有唯一标识与生命周期）
│   │   └── __init__.py
│   ├── value_objects/   # 值对象（无标识、不可变）
│   │   └── __init__.py
│   ├── aggregates/      # 聚合根（外部访问唯一入口）
│   │   └── __init__.py
│   ├── repositories/    # 仓储接口（接口定义，不依赖具体实现）
│   │   └── __init__.py
│   └── services/        # 领域服务（跨聚合的业务操作）
│       └── __init__.py
├── application/         # 应用层（用例编排）
│   ├── __init__.py
│   ├── use_cases/      # 用例（应用服务）
│   │   └── __init__.py
│   └── services/       # 应用服务（协调多个用例）
│       └── __init__.py
├── interface/           # 接口层（API/CLI）
│   ├── __init__.py
│   ├── api/            # API 控制器（FastAPI/Flask）
│   │   └── __init__.py
│   └── cli/            # CLI 命令（Click/Typer）
│       └── __init__.py
└── infrastructure/      # 基础设施层（仓储实现）
    ├── __init__.py
    ├── persistence/    # 数据库实现（SQLAlchemy/Peewee）
    │   └── __init__.py
    ├── external/       # 外部服务客户端（HTTP/RPC）
    │   └── __init__.py
    └── config/         # 配置（环境变量/配置文件）
        └── __init__.py

tests/
├── unit/              # 单元测试（mock 外部依赖）
│   ├── domain/        # 领域层测试
│   ├── application/   # 应用层测试
│   └── interface/     # 接口层测试
└── integration/       # 集成测试（真实依赖）
    └── __init__.py
```

---

## 依赖约定

- **Web 框架**：FastAPI（推荐）或 Flask
- **ORM**：SQLAlchemy
- **CLI**：Typer（推荐）或 Click
- **测试**：pytest + pytest-mock
- **依赖注入**：dependency-injector（可选）

---

## 端口与数据库约定

- **开发端口**：8000（后端）
- **测试端口**：8010
- **开发数据库**：`{project}_dev`
- **测试数据库**：`{project}_test`

---

## 模板文件 vs 业务代码

**模板生成文件**（不测、不删）：
- 所有 `__init__.py` 文件
- `tests/` 目录结构
- 本 `README.md` 文件

**需业务实现文件**（需测试、需实现）：
- `domain/entities/*.py`（业务实体）
- `domain/value_objects/*.py`（业务值对象）
- `domain/aggregates/*.py`（聚合根）
- `domain/repositories/*.py`（仓储接口）
- `domain/services/*.py`（领域服务）
- `application/use_cases/*.py`（用例）
- `interface/api/*.py`（API 控制器）
- `interface/cli/*.py`（CLI 命令）
- `infrastructure/persistence/*.py`（仓储实现）

---

## 实现示例（参考）

### 1. 实体示例（domain/entities/user.py）

```python
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class User:
    id: UUID
    name: str
    email: str

    @classmethod
    def create(cls, name: str, email: str) -> "User":
        return User(id=uuid4(), name=name, email=email)
```

### 2. 仓储接口示例（domain/repositories/user_repository.py）

```python
from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        pass
```

### 3. 用例示例（application/use_cases/create_user.py）

```python
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, name: str, email: str) -> User:
        user = User.create(name=name, email=email)
        self.user_repo.save(user)
        return user
```

---

## 注意事项

1. **依赖方向**：interface → application → domain（外层指向内层）
2. **domain 层零外部依赖**：不引用任何 framework/database/library
3. **跨聚合修改**：经应用服务协调，不直接穿透对象图
4. **实体行为**：状态变化通过领域方法表达（不暴露 setter 裸改）

---

> **维护**：框架维护者 | **最后更新**：2025-08-15
