from datetime import datetime
from typing import Optional

from pydantic import BaseModel,Field
# 增
class ArticleCreate(BaseModel):
    title: str=Field(min_length=2,max_length=15,description="文章名要求2到15个字符")
    content: str
    author: str

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

# 更新
class ArticleUpdate(ArticleCreate):
    pass
