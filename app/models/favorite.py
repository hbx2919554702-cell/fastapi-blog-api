from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, UniqueConstraint, Index, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.users import DBUser
    from app.models.articles import DBArticle

class Favorite(Base):
    __tablename__ = "favorite"

    __table_args__ = (
        UniqueConstraint("user_id","article_id", name="user_id_article_id_unique"),
        Index('fk_favorite_user_idx','user_id'),
        Index('fk_favorite_article_idx','article_id')
    )

    id:Mapped[int]=mapped_column(Integer, primary_key=True,comment="收藏id")
    user_id:Mapped[int]=mapped_column(Integer, ForeignKey("user.id"), nullable=False,comment="用户id")
    article_id:Mapped[int]=mapped_column(Integer,ForeignKey("article.id"),nullable=False,comment="文章id")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=func.now(),nullable=False,comment="创建时间")
    user: Mapped["DBUser"] = relationship(back_populates="favorites")
    article: Mapped["DBArticle"] = relationship(back_populates="favorites")