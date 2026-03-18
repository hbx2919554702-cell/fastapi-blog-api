from datetime import datetime
from typing import Optional

from pydantic import BaseModel
# 增
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: str = "匿名用户"

# 查所有文章
class ArticleResponse(ArticleCreate):
    id:int
    created_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None
    class Config:
        from_attributes = True

# 根据文章id查文章
class ArticleDetail(ArticleCreate):
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        from_attributes = True