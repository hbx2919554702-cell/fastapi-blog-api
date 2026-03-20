from sqlalchemy import Column, DateTime, func, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sympy import false

from app.database import Base


class DBArticle(Base):
    __tablename__ = 'article'
    created_at = Column(DateTime, default=func.now(),comment="发布时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(),comment="更新时间")
    id=Column(Integer,primary_key=True,index=True,comment="文章编号")
    title=Column(String(50),nullable=false,comment="标题")
    content=Column(String(255),comment="内容")
    author_id=Column(Integer, ForeignKey('user.id'),comment="作者")
    owner=relationship("DBUser", back_populates="articles")