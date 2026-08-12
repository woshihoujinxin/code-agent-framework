# E2E 外部依赖启动手册（Redis / MySQL / PostgreSQL / MongoDB）

> **何时读本文件**：E2E 任务**有服务依赖**（Redis/MySQL/PostgreSQL/MongoDB）时。纯 CLI / 文件型 E2E（无服务依赖）**不读本文件**，直接用跨平台临时目录做文件存储即可。

## 支持的依赖类型

| 依赖类型 | 测试策略 | 默认启动方式 |
|----------|----------|--------------|
| **Redis** | 测试容器独立实例 | `docker run -d -p 6379:6379 redis` |
| **MySQL** | 测试容器独立实例 | `docker run -d -p 3306:3306 mysql` |
| **PostgreSQL** | 测试容器独立实例 | `docker run -d -p 5432:5432 postgres` |
| **MongoDB** | 测试容器独立实例 | `docker run -d -p 27017:27017 mongo` |

## 跨平台前置检查（必做）

**不修改系统 Docker 配置**（`/etc/docker/daemon.json` 等）——tester 是只读角色，改系统配置需 root 且仅限 Linux，越界且必然失败。镜像加速通过 `docker run` 时**按次尝试**不同镜像源实现（见下），而非全局改 daemon。

**Docker 可用性检测**：
```bash
docker info >/dev/null 2>&1 && echo "DOCKER=ok" || echo "DOCKER=missing"
```
- `DOCKER=missing` → 设 `SKIP_E2E=true`，报告中记录"无 Docker，跳过依赖型 E2E"，**不报错**（纯 CLI/文件型 E2E 仍可继续）
- 依赖服务健康检查：优先 `redis-cli ping` / `pg_isready` 等客户端；若不可用，用纯标准库 TCP 探测 `python -c "import socket;s=socket.socket();s.settimeout(2);s.connect(('localhost',PORT));print('up')"`

## 依赖启动流程（带国内镜像支持）

以 Redis 为例（其他服务同理，换镜像名/端口/客户端）：

```bash
# 检查本地服务是否运行
if redis-cli ping > /dev/null 2>&1; then
  echo "Redis 已在本地运行"
  export REDIS_URL=redis://localhost:6379/0
else
  # 尝试使用 Docker 启动测试容器
  if command -v docker &> /dev/null; then
    echo "准备启动 Redis 测试容器..."

    # 优先使用国内镜像源
    IMAGE_NAME="redis"

    # 测试能否拉取官方镜像
    if ! docker pull "$IMAGE_NAME" > /dev/null 2>&1; then
      echo "官方镜像拉取失败，尝试阿里云镜像..."
      IMAGE_NAME="registry.cn-hangzhou.aliyuncs.com/library/redis"

      if ! docker pull "$IMAGE_NAME" > /dev/null 2>&1; then
        echo "阿里云镜像也失败，尝试 DaoCloud..."
        IMAGE_NAME="daocloud.io/library/redis"

        if ! docker pull "$IMAGE_NAME" > /dev/null 2>&1; then
          echo "警告：所有镜像源都无法拉取 Redis"
          export SKIP_E2E=true
        fi
      fi
    fi

    # 如果成功获取镜像，启动容器
    if [ -z "$SKIP_E2E" ]; then
      # 停止并清理旧容器
      docker stop test-redis > /dev/null 2>&1 || true
      docker rm test-redis > /dev/null 2>&1 || true

      # 启动新容器
      docker run -d --name test-redis -p 6379:6379 "$IMAGE_NAME"
      sleep 3

      # 等待 Redis 就绪
      MAX_RETRIES=5
      RETRY=0
      while [ $RETRY -lt $MAX_RETRIES ]; do
        if redis-cli ping > /dev/null 2>&1; then
          echo "Redis 容器启动成功"
          export REDIS_URL=redis://localhost:6379/0
          break
        fi
        RETRY=$((RETRY+1))
        sleep 1
      done

      if [ $RETRY -eq $MAX_RETRIES ]; then
        echo "警告：Redis 容器启动超时"
        export SKIP_E2E=true
      fi
    fi
  else
    echo "警告：未安装 Docker，跳过端到端测试"
    export SKIP_E2E=true
  fi
fi

# 设置测试模式
export TEST_MODE=true
```
