from datetime import datetime
from sqlalchemy import  DateTime, func, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import DBUser
    from app.models.favorite import Favorite
    from app.models.comment import Comment
    from app.models.history import History

class DBArticle(Base):
    __tablename__ = 'article'

    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True,comment="文章编号")
    title:Mapped[str]=mapped_column(String(50),nullable=False,comment="标题")
    content:Mapped[str]=mapped_column(String(255),comment="内容")
    created_at:Mapped[datetime]=mapped_column(DateTime, default=func.now(), comment="发布时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    author_id:Mapped[int]=mapped_column(Integer, ForeignKey("user.id"),comment="作者")
    view_count:Mapped[int]=mapped_column(Integer,default=0,comment="浏览量")
    owner:Mapped["DBUser"]=relationship( back_populates="articles")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="article",cascade="all, delete-orphan")
    comments:Mapped[list["Comment"]] = relationship(back_populates="article",cascade="all, delete-orphan")
    history:Mapped[list["History"]] = relationship(back_populates="article")