import pytest
from sqlalchemy.orm import Session

from app.crud.crud_user import (
    get_user,
    get_user_by_username,
    get_user_by_email,
    authenticate_user,
    create_user
)
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def test_get_user(db: Session, test_user):
    """测试通过ID获取用户"""
    user = get_user(db, user_id=test_user.id)
    assert user is not None
    assert user.id == test_user.id
    assert user.username == test_user.username
    assert user.email == test_user.email


def test_get_user_nonexistent(db: Session):
    """测试获取不存在的用户"""
    user = get_user(db, user_id=99999)
    assert user is None


def test_get_user_by_username(db: Session, test_user):
    """测试通过用户名获取用户"""
    user = get_user_by_username(db, username=test_user.username)
    assert user is not None
    assert user.username == test_user.username
    assert user.email == test_user.email


def test_get_user_by_username_nonexistent(db: Session):
    """测试获取不存在的用户名"""
    user = get_user_by_username(db, username="nonexistent")
    assert user is None


def test_get_user_by_email(db: Session, test_user):
    """测试通过邮箱获取用户"""
    user = get_user_by_email(db, email=test_user.email)
    assert user is not None
    assert user.username == test_user.username
    assert user.email == test_user.email


def test_get_user_by_email_nonexistent(db: Session):
    """测试获取不存在的邮箱"""
    user = get_user_by_email(db, email="nonexistent@example.com")
    assert user is None


def test_authenticate_user_success(db: Session, test_user):
    """测试用户认证成功"""
    user = authenticate_user(db, username=test_user.username, password="testpassword")
    assert user is not False
    assert user.username == test_user.username


def test_authenticate_user_wrong_password(db: Session, test_user):
    """测试用户认证密码错误"""
    user = authenticate_user(db, username=test_user.username, password="wrongpassword")
    assert user is False


def test_authenticate_user_nonexistent(db: Session):
    """测试认证不存在的用户"""
    user = authenticate_user(db, username="nonexistent", password="password")
    assert user is False


def test_create_user(db: Session):
    """测试创建用户"""
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="newpassword",
        full_name="New User"
    )
    
    user = create_user(db, obj_in=user_data)
    assert user.username == user_data.username
    assert user.email == user_data.email
    assert user.full_name == user_data.full_name
    assert user.is_active is True
    assert user.is_superuser is False
    
    # 验证密码已被哈希
    assert user.hashed_password != user_data.password
    
    # 验证可以通过新密码认证
    authenticated_user = authenticate_user(db, username=user_data.username, password=user_data.password)
    assert authenticated_user is not False
    assert authenticated_user.id == user.id


def test_create_user_duplicate_username(db: Session, test_user):
    """测试创建重复用户名的用户"""
    user_data = UserCreate(
        username=test_user.username,  # 使用已存在的用户名
        email="different@example.com",
        password="password",
        full_name="Different User"
    )
    
    # 这应该会引发异常或返回None，具体取决于实现
    # 由于我们的create_user函数没有处理重复，这里可能会引发数据库异常
    with pytest.raises(Exception):
        create_user(db, obj_in=user_data)


def test_create_user_duplicate_email(db: Session, test_user):
    """测试创建重复邮箱的用户"""
    user_data = UserCreate(
        username="differentuser",
        email=test_user.email,  # 使用已存在的邮箱
        password="password",
        full_name="Different User"
    )
    
    # 这应该会引发异常或返回None，具体取决于实现
    with pytest.raises(Exception):
        create_user(db, obj_in=user_data)