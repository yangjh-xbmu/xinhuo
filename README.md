# 薪火项目

一个基于 Docker 的全栈 Web 应用，包含 Next.js 前端、FastAPI 后端和 PostgreSQL 数据库。

## 环境前提条件

在开始之前，请确保您的系统已安装以下软件：

- **Git** - 用于克隆代码仓库
- **Docker** (版本 20.10 或更高) - 容器化平台
- **Docker Compose** (版本 2.0 或更高) - 多容器应用编排工具

**Windows 用户特别注意**：

- 需要配置好 **WSL2 (Windows Subsystem for Linux 2)**
- 确保 Docker Desktop 已启用 WSL2 集成

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd xinhuo
```

### 2. 环境配置

**复制环境变量模板**

```bash
cp .env.example .env
```

**编辑环境变量**（可选）

`.env.example` 文件已包含默认配置，可直接使用。如需自定义，请编辑 `.env` 文件：

```bash
# aipm configuration
LLM_API_KEY='your_api_key_here'

# Database Configuration
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database_name

# Database URL for backend connection
DATABASE_URL=postgresql://your_username:your_password@db:5432/your_database_name
```

### 3. 启动应用

```bash
docker-compose up -d
```

此命令将启动所有服务（前端、后端、数据库）并在后台运行。

### 4. 验证步骤

**检查服务状态**

```bash
docker-compose ps
```

所有服务应显示为 "Up" 状态。

**访问应用**

- 前端应用：打开浏览器访问 [http://localhost:3000](http://localhost:3000)
- 后端 API：访问 [http://localhost:8000](http://localhost:8000)
- API 文档：访问 [http://localhost:8000/docs](http://localhost:8000/docs) 查看自动生成的交互式 API 文档

**端到端验证**

前端页面应成功请求并展示来自后端的 "Hello World" 消息，这表明：

- 前端服务正常运行
- 后端 API 正常响应
- 服务间网络通信正常
- 整个应用栈配置正确

### 5. 停止应用

```bash
docker-compose down
```

## 项目结构

```
├── frontend/          # Next.js 前端应用
│   ├── src/app/       # 应用页面和组件
│   ├── Dockerfile.dev # 前端开发环境 Docker 配置
│   └── package.json   # 前端依赖配置
├── backend/           # FastAPI 后端应用
│   ├── app/           # 后端应用代码
│   │   └── main.py    # 主应用文件，包含 API 路由
│   ├── Dockerfile     # 后端 Docker 配置
│   └── requirements.txt # 后端 Python 依赖
├── docker-compose.yml # Docker Compose 多服务编排配置
├── .env              # 环境变量配置（不提交到 Git）
├── .env.example      # 环境变量模板
└── README.md         # 项目说明文档
```

### 目录说明

- **`/frontend`**: Next.js 前端应用，负责用户界面展示和与后端 API 的交互
- **`/backend`**: FastAPI 后端应用，提供 RESTful API 服务和数据库交互
- **`docker-compose.yml`**: 定义了前端、后端、数据库三个服务的容器化配置

## 代码热重载功能

本项目在开发环境中支持代码热重载，大大提升开发效率：

### 前端热重载

- **自动检测**: 修改 `/frontend` 目录下的任何文件后，Next.js 会自动检测变化
- **即时更新**: 浏览器页面会自动刷新，无需手动重启服务
- **保持状态**: 在大多数情况下，应用状态会被保留

### 后端热重载

- **文件监控**: FastAPI 使用 `--reload` 参数启动，监控 Python 文件变化
- **自动重启**: 修改 `/backend` 目录下的 `.py` 文件后，服务会自动重启
- **快速生效**: 新的 API 变更立即生效，无需手动操作

### 使用示例

1. 修改 `/frontend/src/app/page.tsx` 中的文本内容
2. 保存文件后，浏览器页面自动更新显示新内容
3. 修改 `/backend/app/main.py` 中的 API 响应
4. 保存文件后，后端服务自动重启，新的 API 响应立即生效

## 功能特性

- ✅ **Docker 容器化部署** - 一键启动完整开发环境
- ✅ **环境变量配置管理** - 安全的配置文件管理
- ✅ **数据持久化存储** - PostgreSQL 数据在容器重启后保持
- ✅ **代码热重载支持** - 前后端代码修改后自动生效
- ✅ **前后端服务通信** - 完整的端到端数据流
- ✅ **API 文档自动生成** - FastAPI 自动生成交互式 API 文档

## 开发说明

- **环境变量管理**: 所有敏感信息通过 `.env` 文件管理，该文件已被 `.gitignore` 排除
- **数据持久化**: 数据库数据通过 Docker 命名数据卷持久化存储，容器重启后数据不丢失
- **开发效率**: 支持代码热重载，修改代码后无需手动重启服务
- **首次启动**: 按照本文档操作，从克隆到运行成功应在 15 分钟内完成

## 常见问题

**Q: 服务启动失败怎么办？**
A: 检查 Docker 是否正常运行，端口 3000、8000、5432 是否被占用

**Q: 前端页面无法显示后端数据？**
A: 确认所有服务都已启动，检查 `docker-compose ps` 输出

**Q: 如何查看服务日志？**
A: 使用 `docker-compose logs [service-name]` 查看特定服务日志
