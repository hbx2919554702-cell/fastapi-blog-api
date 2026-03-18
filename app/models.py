from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class DBArticle(Base):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    __tablename__='article'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(50))
    content=Column(String(200))
    author=Column(String(20), default='匿名用户')
