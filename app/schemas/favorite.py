from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.articles import ArticleShow

# 查看收藏状态
class FavoriteResponse(BaseModel):
    is_favorite: bool=Field(...,alias="isFavorite")

# 添加收藏请求
class FavoriteAddRequest(BaseModel):
    article_id: int = Field(...,alias="articleId")

# 删除收藏请求
class FavoriteDeleteRequest(BaseModel):
    article_id: int = Field(..., alias="articleId")

# 封装响应数据
class FavoriteArticleResponse(ArticleShow):
    favorite_id: int = Field(...,alias="favoriteId")
    favorite_at:datetime=Field(...,alias="favoriteAt")

class FavoriteListResponse(BaseModel):
    list:list [FavoriteArticleResponse]
    total: int
    has_more: bool=Field(...,alias="hasMore")