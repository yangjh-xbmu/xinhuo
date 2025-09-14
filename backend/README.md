# 薪火后端

基于 FastAPI 的后端服务，提供用户认证和管理功能。

## 功能特性

- 🔐 JWT 用户认证系统
- 👤 用户管理（注册、登录、权限控制）
- 🛡️ 密码安全哈希存储
- 📊 PostgreSQL 数据库支持
- 🧪 完整的单元测试和集成测试
- 📚 自动生成的 API 文档

## 快速开始

### 1. 环境配置

复制环境变量模板并配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件，设置以下变量：
```env
# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 数据库配置
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
DATABASE_URL=postgresql://your_username:your_password@localhost/your_database
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库迁移

```bash
# 初始化数据库
alembic upgrade head
```

### 4. 运行开发服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 认证系统

### 登录

```bash
curl -X POST "http://localhost:8000/api/v1/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=your_username&password=your_password"
```

### 使用 JWT Token

```bash
curl -X GET "http://localhost:8000/api/v1/protected-endpoint" \
     -H "Authorization: Bearer your_jwt_token"
```

## 测试

运行所有测试：
```bash
pytest tests/ -v
```

运行特定测试文件：
```bash
pytest tests/test_auth.py -v
```

## 项目结构

```
backend/
├── app/
│   ├── api/                 # API 路由
│   │   └── v1/
│   │       ├── api.py       # 主路由器
│   │       └── endpoints/   # 端点实现
│   │           └── login.py # 登录端点
│   ├── core/                # 核心功能
│   │   ├── config.py        # 配置管理
│   │   ├── security.py      # 安全功能
│   │   └── dependencies.py  # 依赖注入
│   ├── crud/                # 数据库操作
│   │   └── crud_user.py     # 用户 CRUD
│   ├── db/                  # 数据库配置
│   │   ├── base.py          # 数据库基础配置
│   │   └── init_db.py       # 数据库初始化
│   ├── models/              # 数据模型
│   │   └── user.py          # 用户模型
│   ├── schemas/             # Pydantic 模式
│   │   ├── token.py         # Token 模式
│   │   └── user.py          # 用户模式
│   └── main.py              # 应用入口
├── tests/                   # 测试文件
│   ├── conftest.py          # 测试配置
│   ├── test_auth.py         # 认证测试
│   ├── test_crud_user.py    # CRUD 测试
│   └── test_security.py     # 安全功能测试
├── alembic/                 # 数据库迁移
├── requirements.txt         # 依赖列表
└── README.md               # 项目文档
```

## 开发指南

### 添加新的 API 端点

1. 在 `app/api/v1/endpoints/` 中创建新的端点文件
2. 在 `app/api/v1/api.py` 中注册路由
3. 添加相应的测试文件

### 数据库模型变更

1. 修改 `app/models/` 中的模型
2. 生成迁移文件：`alembic revision --autogenerate -m "描述"`
3. 应用迁移：`alembic upgrade head`

## Docker 部署

### 构建镜像

```bash
docker build -t xinhuo-backend .
```

### 运行容器

```bash
# 后台运行
docker run -d --name xinhuo-backend -p 8000:80 --restart unless-stopped xinhuo-backend

# 查看日志
docker logs -f xinhuo-backend

# 健康检查
curl -i http://localhost:8000/
```

## 安全注意事项

- 🔑 确保 `SECRET_KEY` 足够复杂且保密
- 🔒 生产环境中使用 HTTPS
- 🛡️ 定期更新依赖包
- 📝 不要在代码中硬编码敏感信息

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。