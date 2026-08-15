# Java DDD 四层目录模板

> **模板来源**：DDD 经典结构适配 Java（Spring Boot）
> **适用场景**：标准 DDD + 业务规则复杂的项目

---

## 目录结构

```
src/
└── main/
    └── java/
        └── com/
            └── example/
                └── {project}/
                    ├── domain/              # 领域层（零外部依赖）
                    │   ├── model/           # 领域模型
                    │   │   ├── entity/      # 实体（JPA Entity）
                    │   │   ├── valueobject/ # 值对象（@Embeddable）
                    │   │   └── aggregate/   # 聚合根
                    │   ├── repository/      # 仓储接口（Spring Data）
                    │   └── service/         # 领域服务（@DomainService）
                    ├── application/         # 应用层（用例编排）
                    │   ├── usecase/        # 用例（ApplicationService）
                    │   └── dto/            # 数据传输对象
                    ├── interface/          # 接口层（API/CLI）
                    │   ├── api/            # REST 控制器（@RestController）
                    │   └── cli/            # CLI 命令（Spring Shell）
                    └── infrastructure/     # 基础设施层（仓储实现）
                        ├── persistence/     # JPA 实现（Repository Impl）
                        ├── external/        # 外部服务客户端（RestTemplate/WebClient）
                        └── config/          # Spring 配置（@Configuration）
src/test/java/                       # 单元测试（JUnit 5 + Mockito）
    └── com/example/{project}/
        ├── domain/                    # 领域层测试
        ├── application/              # 应用层测试
        └── interface/                 # 接口层测试
```

---

## 依赖约定

- **运行时**：Java >= 17
- **框架**：Spring Boot >= 3.2
- **构建**：Maven 或 Gradle
- **JPA**：Spring Data JPA + Hibernate
- **测试**：JUnit 5 + Mockito
- **CLI**：Spring Shell（可选）
- **验证**：Jakarta Validation

---

## 端口与数据库约定

- **开发端口**：8080（后端）
- **测试端口**：8090
- **开发数据库**：`{project}_dev`（H2/PostgreSQL）
- **测试数据库**：`{project}_test`（H2 内存）

---

## 模板文件 vs 业务代码

**模板生成文件**（不测、不删）：
- `pom.xml` 或 `build.gradle`
- `src/main/resources/application.yml`
- `tests/` 目录结构
- 本 `README.md` 文件

**需业务实现文件**（需测试、需实现）：
- `src/main/java/.../domain/model/entity/*.java`
- `src/main/java/.../domain/model/valueobject/*.java`
- `src/main/java/.../domain/model/aggregate/*.java`
- `src/main/java/.../domain/repository/*.java`
- `src/main/java/.../domain/service/*.java`
- `src/main/java/.../application/usecase/*.java`
- `src/main/java/.../interface/api/*.java`
- `src/main/java/.../infrastructure/persistence/*.java`

---

## 实现示例（参考）

### 1. 实体示例（domain/model/entity/User.java）

```java
package com.example.{project}.domain.model.entity;

import jakarta.persistence.*;
import java.util.UUID;

@Entity
@Table(name = "users")
public class User {
    @Id
    private UUID id;
    private String name;
    private String email;

    protected User() {} // JPA

    public static User create(String name, String email) {
        User user = new User();
        user.id = UUID.randomUUID();
        user.name = name;
        user.email = email;
        return user;
    }

    public UUID getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

### 2. 仓储接口示例（domain/repository/UserRepository.java）

```java
package com.example.{project}.domain.repository;

import com.example.{project}.domain.model.entity.User;
import java.util.Optional;
import java.util.UUID;

public interface UserRepository {
    void save(User user);
    Optional<User> findById(UUID id);
}
```

### 3. 用例示例（application/usecase/CreateUserUseCase.java）

```java
package com.example.{project}.application.usecase;

import com.example.{project}.domain.model.entity.User;
import com.example.{project}.domain.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class CreateUserUseCase {
    private final UserRepository userRepo;

    public CreateUserUseCase(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    public User execute(String name, String email) {
        User user = User.create(name, email);
        userRepo.save(user);
        return user;
    }
}
```

---

## 注意事项

1. **依赖方向**：interface → application → domain（外层指向内层）
2. **domain 层零外部依赖**：不引用 Spring/Framework（除 JPA 注解）
3. **跨聚合修改**：经应用服务协调，不直接穿透对象图
4. **实体行为**：状态变化通过工厂方法/领域方法表达
5. **包命名**：遵循 Java 约定，全小写，点分隔

---

> **维护**：框架维护者 | **最后更新**：2025-08-15
