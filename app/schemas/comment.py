from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict, AliasPath


# 发表评论
class AddComment(BaseModel):
    article_id: int=Field(...,description="文章id",json_schema_extra={"example": ""})
    comment: str=Field(...,min_length=1,max_length=500,description="评论要求1到500个字符",json_schema_extra={"example": ""})


# 封装响应数据
class CommentArticleResponse(BaseModel):
    id: int = Field(..., description="评论的唯一ID")
    article_id: int = Field(..., description="所属文章ID")
    content: str = Field(..., description="评论内容",validation_alias="comment")
    user_id: int = Field(..., description="评论者用户ID")
    nickname : str = Field(validation_alias=AliasPath("user","nickname"),description="评论者用户昵称")
    created_at:datetime =Field(...,description="评论发表时间")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class CommentListResponse(BaseModel):
    list: list[CommentArticleResponse]
    total: int
    hasMore: bool=Field(...,alias="hasMore")
