from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class DBUser(Base):
    __tablename__ = 'user'
    id=Column(Integer,primary_key=True,index=True,comment="用户编号")
    hashed_password=Column(String(255),nullable=False,comment="用户密码")
    username=Column(String(50),unique=True,index=True,nullable=False,comment="用户名")
    email=Column(String(255),nullable=True,comment="电子邮箱(选填)")
    nickname = Column(String(50), nullable=True,default="匿名用户",comment="昵称")
    gender = Column(String(10), nullable=True, comment="性别")
    bio = Column(String(255), nullable=True, default="这个人很懒，什么都没有留下",comment="简介")
    articles=relationship("DBArticle", back_populates="owner")