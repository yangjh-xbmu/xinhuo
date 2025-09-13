from fastapi import FastAPI

app = FastAPI(title="薪火后端API", description="薪火项目的后端服务")


@app.get("/")
def read_root():
    return {"message": "来自薪火后端的问候"}