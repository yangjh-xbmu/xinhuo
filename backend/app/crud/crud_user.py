from typing import Optional, Union

from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash, verify_password


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    根据用户ID获取用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
    
    Returns:
        用户对象或None
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名获取用户
    
    Args:
        db: 数据库会话
        username: 用户名
    
    Returns:
        用户对象或None
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    根据邮箱获取用户
    
    Args:
        db: 数据库会话
        email: 邮箱地址
    
    Returns:
        用户对象或None
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    """
    验证用户身份
    
    Args:
        db: 数据库会话
        username: 用户名
        password: 密码
    
    Returns:
        验证成功返回用户对象，否则返回False
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, *, obj_in: UserCreate) -> User:
    """
    创建新用户
    
    Args:
        db: 数据库会话
        obj_in: 用户创建数据
    
    Returns:
        创建的用户对象
    """
    hashed_password = get_password_hash(obj_in.password)
    db_user = User(
        username=obj_in.username,
        email=obj_in.email,
        hashed_password=hashed_password,
        full_name=obj_in.full_name,
        is_active=obj_in.is_active,
        is_superuser=obj_in.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user