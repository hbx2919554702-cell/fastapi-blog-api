#######################文章#####################
# 增
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict,AliasPath


# 创建文章
class ArticleCreate(BaseModel):
    title: str=Field(min_length=2,max_length=25,description="文章名要求2到25个字符",json_schema_extra={"example": ""})
    content: str=Field(min_length=1,description="文章内容不能为空",json_schema_extra={"example": ""})

# 查所有文章
class ArticleResponse(ArticleCreate):
    id:int
    author_id:int
    nickname : str = Field(validation_alias=AliasPath("owner","nickname"))
    created_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None
    view_count:int
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 根据文章id查文章
class ArticleDetail(ArticleCreate):
    id: int
    author_id: int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    nickname : str = Field(validation_alias=AliasPath("owner","nickname"))
    view_count: int

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# 更新
class ArticleUpdate(ArticleCreate):
    pass


class ArticleShow(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime]=None
    nickname : str = Field(validation_alias=AliasPath("owner","nickname"))
    view_count: int

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )