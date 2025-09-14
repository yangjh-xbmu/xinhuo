from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..db.base import get_db
from ..crud.crud_user import get_user_by_username
from ..models.user import User
from ..schemas.token import TokenData
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    获取当前用户依赖项
    
    Args:
        token: JWT令牌
        db: 数据库会话
    
    Returns:
        当前用户对象
    
    Raises:
        HTTPException: 当令牌无效或用户不存在时
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户依赖项
    
    Args:
        current_user: 当前用户
    
    Returns:
        当前活跃用户对象
    
    Raises:
        HTTPException: 当用户未激活时
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_teacher_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    获取当前教师用户依赖项
    
    Args:
        current_user: 当前用户
    
    Returns:
        当前教师用户对象
    
    Raises:
        HTTPException: 当用户不是教师时
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user