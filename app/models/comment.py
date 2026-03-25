from datetime import datetime
from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy import Integer, ForeignKey, Text, DateTime, func, Index
from sqlalchemy.orm import Mapped, relationship,mapped_column

if TYPE_CHECKING:
    from app.models.users import DBUser
    from app.models.articles import DBArticle

class Comment(Base):
    __tablename__ = 'comment'

    __table_args__ = (
        Index('fk_comment_user_idx', 'user_id'),
        Index('fk_comment_article_idx', 'article_id'),
    )

    id:Mapped[int]=mapped_column(Integer, primary_key=True,index=True,comment="id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"),nullable=False,comment="user_id")
    article_id:Mapped[int]=mapped_column(Integer,ForeignKey("article.id"),nullable=False,comment="article_id")
    comment:Mapped[str]=mapped_column(Text,nullable=False,comment="评论")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=func.now(),nullable=False,comment="创建时间")
    user:Mapped["DBUser"]=relationship(back_populates="comments")
    article:Mapped["DBArticle"]=relationship(back_populates="comments")
