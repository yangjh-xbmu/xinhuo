import pytest
from jose import jwt
from datetime import datetime, timedelta

from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash
)
from app.core.config import settings


def test_create_access_token():
    """测试创建访问令牌"""
    username = "testuser"
    token = create_access_token(subject=username)
    
    # 解码令牌验证内容
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == username
    assert "exp" in payload
    
    # 验证过期时间
    exp_timestamp = payload["exp"]
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
    now = datetime.utcnow()
    expected_exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 允许1分钟的误差
    assert abs((exp_datetime - expected_exp).total_seconds()) < 60


def test_create_access_token_with_custom_expiry():
    """测试创建带自定义过期时间的访问令牌"""
    username = "testuser"
    expires_delta = timedelta(minutes=60)
    token = create_access_token(subject=username, expires_delta=expires_delta)
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp_timestamp = payload["exp"]
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
    now = datetime.utcnow()
    expected_exp = now + expires_delta
    
    # 允许1分钟的误差
    assert abs((exp_datetime - expected_exp).total_seconds()) < 60


def test_password_hashing():
    """测试密码哈希功能"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # 哈希值应该与原密码不同
    assert hashed != password
    
    # 验证密码应该成功
    assert verify_password(password, hashed) is True
    
    # 错误密码应该验证失败
    assert verify_password("wrongpassword", hashed) is False


def test_password_hash_uniqueness():
    """测试相同密码的哈希值应该不同（由于盐值）"""
    password = "testpassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # 两次哈希应该不同（bcrypt使用随机盐值）
    assert hash1 != hash2
    
    # 但都应该能验证原密码
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True