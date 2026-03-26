from pydantic import BaseModel, Field

from app.schemas.articles import ArticleShow


class HistoryListResponse(BaseModel):
    list: list[ArticleShow]
    total:int
    has_more:bool=Field(...,alias="hasMore")