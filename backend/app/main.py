from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router

app = FastAPI(title="薪火后端API", description="薪火项目的后端服务")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册API路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "来自薪火后端的问候 - 热重载功能已验证 ✅"}