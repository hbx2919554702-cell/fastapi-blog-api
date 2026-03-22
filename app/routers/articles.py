from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.depends import get_current_user
from app.database import get_db
from app.models import articles
from app.schemas.articles import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleDetail
from app.crud import articles
router = APIRouter(prefix="/api/articles", tags=["articles"])

# 创建文章
@router.post("/create", response_model=ArticleResponse)
def create_article(article:ArticleCreate,
                   db:Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    return articles.create_article(db=db,article=article,author_id=current_user.id)


# 根据id搜索文章
@router.get("/get_articles_id/{article_id}", response_model=ArticleDetail)
def get_articles_id(article_id:int,db:Session = Depends(get_db)):
    db_article_id = articles.get_article_id(article_id=article_id,db=db)
    if db_article_id is None:
        raise HTTPException(status_code=404,detail='文章不存在')
    return db_article_id

# 模糊搜索
@router.get("/get_articles", response_model=List[ArticleResponse])
def get_articles(page:int=Query(1,ge=1,description="请求的页码从1开始"),
                 limit:int=Query(10,gt=1,le=20,description="每页数量"),
                 keyword:Optional[str]=Query(None,description="搜索文章标题关键字"),
                 db:Session = Depends(get_db)):
    skip=(page-1)*limit
    db_articles = articles.get_articles(skip=skip,limit=limit,keyword=keyword,db=db)
    return db_articles

# 更新文章
@router.put("/update/{article_id}", response_model=ArticleUpdate)
def update_article(article_id:int,article: ArticleUpdate,
                   db:Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    db_article=get_articles_id(article_id=article_id,db=db)
    if db_article is None:
        raise HTTPException(status_code=404,detail="文章不存在")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403,detail="无法更改文章")
    update_article=articles.update_article(db_article=db_article,update_article=article,db=db)
    return update_article

# 删除文章
@router.delete("/delete/{article_id}")
def delete_article(article_id:int,db:Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    db_article=get_articles_id(article_id, db)
    if db_article is None:
        raise HTTPException(status_code=404,detail="文章不存在")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403,detail="你无法删除该文章")
    articles.delete_article(article_id=article_id,db=db)
    return {"message:",f"ID为{article_id}的文章删除成功"}