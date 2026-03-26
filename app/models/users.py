from typing import Optional
from sqlalchemy import Integer, String, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.articles import DBArticle
    from app.models.favorite import Favorite
    from app.models.comment import Comment
    from app.models.history import History

class DBUser(Base):
    __tablename__ = 'user'

    __table_args__ = (
        Index('username_UNIQUE', 'username', unique=True),
    )

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="用户编号")
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False,comment="用户密码")
    username:Mapped[str]=mapped_column(String(50),nullable=False,comment="用户名")
    email:Mapped[str]=mapped_column(String(255),nullable=True,comment="电子邮箱(选填)")
    nickname :Mapped[Optional[str]]=mapped_column(String(50),default="匿名用户",comment="昵称")
    gender:Mapped[Optional[str]]=mapped_column(String(10), nullable=True, comment="性别")
    bio:Mapped[Optional[str]]=mapped_column(String(255), nullable=True, default="这个人很懒，什么都没有留下",comment="简介")
    articles:Mapped[list["DBArticle"]]=relationship(back_populates="owner")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")
    comments:Mapped[list["Comment"]] = relationship(back_populates="user")
    history: Mapped[list["History"]] = relationship(back_populates="user")