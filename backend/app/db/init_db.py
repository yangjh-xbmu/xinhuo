"""数据库初始化脚本"""
from sqlalchemy import create_engine
from .base import Base, DATABASE_URL
import logging

logger = logging.getLogger(__name__)


def create_tables():
    """创建所有数据库表"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        raise


def init_db():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    create_tables()
    logger.info("数据库初始化完成")


if __name__ == "__main__":
    init_db()