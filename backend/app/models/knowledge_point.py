from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.base import Base


class KnowledgePoint(Base):
    """知识点模型"""
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)  # 在课程中的顺序
    
    # 题目相关字段
    quiz_question = Column(Text, nullable=True)  # 练习题题目
    quiz_options = Column(JSON, nullable=True)  # 选择题选项 [{"key": "A", "value": "选项内容"}, ...]
    quiz_correct_answer = Column(String(10), nullable=True)  # 正确答案（如 "A", "B", "C", "D"）
    quiz_explanation = Column(Text, nullable=True)  # 答案解析
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关系
    course = relationship("Course", back_populates="knowledge_points")
    quiz_records = relationship("QuizRecord", back_populates="knowledge_point")
    
    def __repr__(self):
        return f"<KnowledgePoint(id={self.id}, title='{self.title}', course_id={self.course_id})>"