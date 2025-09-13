# Backend (FastAPI + Uvicorn) Docker 运行手册

最后更新：2025-09-13

本手册记录了后端镜像的构建、启动、日常运维与常见问题排查流程，覆盖本次“docker run 看起来无反应”的分析与解决经验。

---

## 1. 快速开始（推荐后台运行）

前置：确保 Docker Desktop/daemon 正常运行（`docker info` 应能返回信息）。

- 构建镜像
  - `docker build -t xinhuo-backend .`
- 启动容器（后台、自启动）
  - `docker run -d --name xinhuo-backend -p 8000:80 --restart unless-stopped xinhuo-backend`
- 访问
  - 健康检查：首页：`curl -i http://localhost:8000/`
  - 文档：`http://localhost:8000/docs`
- 查看状态
  - `docker ps --filter name=xinhuo-backend`
- 查看日志
  - `docker logs -f xinhuo-backend`

说明：容器内服务监听 80 端口，对外映射为宿主 8000（`-p 8000:80`）。

---

## 2. 常用维护操作

- 重启：`docker restart xinhuo-backend`
- 停止：`docker stop xinhuo-backend`
- 删除：`docker rm -f xinhuo-backend`
- 进入容器排查：`docker exec -it xinhuo-backend sh`

---

## 3. 本次“run 无反应”的根因与结论

现象：执行 `docker run …` 时终端看似没有返回，或之前出现过“Cannot connect to the Docker daemon”。

结论：
- 可能原因 A：当时 Docker Desktop/daemon 尚未就绪，导致 CLI 无法与 daemon 建立连接。
- 可能原因 B：`docker run` 未加 `-d`，前台日志占用终端，看起来像“无响应”，实际上容器已在跑。

验证结果：
- 通过 `docker create` → `docker start` → `docker logs -f` 的可观测序列确认 uvicorn 正常启动；
- `curl http://localhost:8000/` 返回 200 OK，`/docs` 可访问；
- 最终改为后台容器 `xinhuo-backend`，并设置 `--restart unless-stopped`。

---

## 4. 排障范式（强烈推荐）

当 `docker run` 行为不明确时，使用以下序列替代直接 `run`：

1) 创建但不启动
- `docker create --name xinhuo-backend-test -p 8000:80 xinhuo-backend`

2) 启动并观察
- `docker start xinhuo-backend-test`
- `docker ps -a --filter name=xinhuo-backend-test`

3) 精确查看状态与错误
- `docker inspect -f 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' xinhuo-backend-test`

4) 拉取日志
- `docker logs -f --tail 200 xinhuo-backend-test`

5) 结束/清理
- `docker rm -f xinhuo-backend-test`

好处：将“创建/启动/观察日志/查看错误”拆分，避免前台卡住终端造成的错觉，并清晰定位失败阶段。

---

## 5. 常见问题与对策清单（Checklist）

- Daemon 未就绪 / 无法连接
  - 现象：`Cannot connect to the Docker daemon`。
  - 对策：确认 Docker Desktop 已启动；`docker info` 应返回正常信息。

- 终端被前台日志占用
  - 现象：`docker run` 无 `-d`，uvicorn 在前台输出；看似“无返回”。
  - 对策：加 `-d` 后台运行，或用“排障范式”的 create→start→logs。

- 名称冲突
  - 现象：`Conflict. The container name "..." is already in use`。
  - 对策：`docker ps -a` 找到同名容器并 `docker rm -f`。

- 端口占用
  - 现象：映射端口启动失败或访问异常。
  - 对策：
    - 检查：macOS 可 `lsof -i :8000`；
    - 换端口映射：如 `-p 18000:80`；
    - 或停止占用该端口的服务。

- 镜像不一致/过旧
  - 对策：`docker build -t xinhuo-backend .` 重新构建；`docker image ls | grep xinhuo-backend` 查看版本；必要时删旧镜像后重建。

- 应用层问题（容器内）
  - 进入容器：`docker exec -it xinhuo-backend sh`
  - 快速自检：
    - `python -V`
    - `pip show uvicorn`
    - `uvicorn app.main:app --host 0.0.0.0 --port 80`（必要时手动重启以复现问题）

---

## 6. 配置与约定

- 镜像启动命令（来自镜像 Cmd）：
  - `["uvicorn","app.main:app","--host","0.0.0.0","--port","80"]`
- 依赖：`requirements.txt` 中已包含 `uvicorn[standard]==0.24.0`
- 端口：容器内 80，对外默认映射宿主 8000。

---

## 7. 最小 Docker Compose 示例（可选）

以下仅作为后续演进的选项，当前无需依赖：

```yaml
services:
  backend:
    image: xinhuo-backend
    container_name: xinhuo-backend
    ports:
      - "8000:80"
    restart: unless-stopped
```

使用：`docker compose up -d`，查看：`docker compose ps`，日志：`docker compose logs -f backend`。

---

## 8. 常用命令速查

- 构建：`docker build -t xinhuo-backend .`
- 启动（后台）：`docker run -d --name xinhuo-backend -p 8000:80 --restart unless-stopped xinhuo-backend`
- 日志：`docker logs -f xinhuo-backend`
- 状态：`docker ps --filter name=xinhuo-backend`
- 清理：`docker rm -f xinhuo-backend`

---

如需补充更多场景或将其自动化（脚本/Compose），请在此文档继续沉淀。