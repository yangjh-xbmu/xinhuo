import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token


def test_login_success(client: TestClient, test_user):
    """测试登录成功"""
    response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # 验证JWT令牌
    token = data["access_token"]
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "testuser"


def test_login_invalid_username(client: TestClient):
    """测试无效用户名登录"""
    response = client.post(
        "/api/v1/login",
        data={"username": "nonexistent", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_invalid_password(client: TestClient, test_user):
    """测试无效密码登录"""
    response = client.post(
        "/api/v1/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_access_protected_route_with_valid_token(client: TestClient, test_user):
    """测试使用有效令牌访问受保护路由"""
    # 创建访问令牌
    access_token = create_access_token(subject=test_user.username)
    
    # 这里需要一个受保护的路由来测试，暂时跳过
    # response = client.get(
    #     "/api/v1/users/me",
    #     headers={"Authorization": f"Bearer {access_token}"}
    # )
    # assert response.status_code == 200
    pass


def test_access_protected_route_without_token(client: TestClient):
    """测试不带令牌访问受保护路由"""
    # 这里需要一个受保护的路由来测试，暂时跳过
    # response = client.get("/api/v1/users/me")
    # assert response.status_code == 401
    pass


def test_access_protected_route_with_invalid_token(client: TestClient):
    """测试使用无效令牌访问受保护路由"""
    # 这里需要一个受保护的路由来测试，暂时跳过
    # response = client.get(
    #     "/api/v1/users/me",
    #     headers={"Authorization": "Bearer invalid_token"}
    # )
    # assert response.status_code == 401
    pass