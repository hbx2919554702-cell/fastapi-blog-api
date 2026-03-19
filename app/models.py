from pydoc import describe

from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class DBArticle(Base):
    __tablename__ = 'article'
    created_at = Column(DateTime, default=func.now(),comment="发布时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(),comment="更新时间")
    id=Column(Integer,primary_key=True,index=True,comment="文章编号")
    title=Column(String(50),comment="标题")
    content=Column(String(255),comment="内容")
    author_id=Column(Integer, ForeignKey('user.id'),comment="作者")
    owner=relationship("DBUser", back_populates="articles")

class DBUser(Base):
    __tablename__ = 'user'
    id=Column(Integer,primary_key=True,index=True,comment="用户编号")
    hashed_password=Column(String(255),nullable=False,comment="用户密码")
    username=Column(String(50),unique=True,index=True,nullable=False,comment="用户名")
    email=Column(String(255),nullable=True,comment="电子邮箱(选填)")
    articles=relationship("DBArticle", back_populates="owner")