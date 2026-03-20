#######################文章#####################
# 增
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# 创建文章
class ArticleCreate(BaseModel):
    title: str=Field(min_length=2,max_length=15,description="文章名要求2到15个字符",json_schema_extra={"example": ""})
    content: str=Field(min_length=1,description="文章内容不能为空",json_schema_extra={"example": ""})
    author_id: int

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