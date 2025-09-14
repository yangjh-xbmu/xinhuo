from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.base import Base


class QuizRecord(Base):
    """答题记录模型"""
    __tablename__ = "quiz_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False, index=True)
    
    # 答题信息
    user_answer = Column(String(10), nullable=False)  # 用户选择的答案（如 "A", "B", "C", "D"）
    is_correct = Column(Boolean, nullable=False)  # 是否答对
    time_spent = Column(Integer, nullable=True)  # 答题用时（秒）
    
    # 可选的反馈信息
    feedback = Column(Text, nullable=True)  # 用户反馈或备注
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="quiz_records")
    knowledge_point = relationship("KnowledgePoint", back_populates="quiz_records")
    
    def __repr__(self):
        return f"<QuizRecord(id={self.id}, user_id={self.user_id}, knowledge_point_id={self.knowledge_point_id}, is_correct={self.is_correct})>"