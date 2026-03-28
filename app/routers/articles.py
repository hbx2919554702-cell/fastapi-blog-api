from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.depends import get_current_user, get_current_user_optional
from app.core.response import success_response
from app.crud.history import add_history
from app.database import get_db
from app.schemas.articles import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleDetail
from app.crud import articles as crud_articles

router = APIRouter(prefix="/api/articles", tags=["articles"])

# 创建文章
@router.post("/create")
async def create_article(article:ArticleCreate,
                   db:AsyncSession= Depends(get_db),
                   current_user=Depends(get_current_user)):
    data= await crud_articles.create_article(db=db,article=article,author_id=current_user.id)
    return success_response(message="创建成功",data=data)

# 根据id搜索文章
@router.get("/get_articles_id/{article_id}")
async def get_articles_id(article_id:int,db:AsyncSession = Depends(get_db),current_user=Depends(get_current_user_optional)):
    db_article_id = await crud_articles.get_article_id(article_id=article_id,db=db)
    if db_article_id is None:
        raise HTTPException(status_code=404,detail='文章不存在')
    data=ArticleDetail.model_validate(db_article_id)
    if current_user:
        await add_history(db=db,article_id=article_id,user_id=current_user.id)
    return success_response(message="查询成功",data=data)


# 模糊搜索
@router.get("/get_articles")
async def get_articles(page:int=Query(1,ge=1,description="请求的页码从1开始"),
                 limit:int=Query(10,gt=1,le=20,description="每页数量"),
                 keyword:Optional[str]=Query(None,description="搜索文章标题关键字"),
                 author_id:Optional[int]=None,
                 db:AsyncSession = Depends(get_db)):
    skip=(page-1)*limit
    db_articles = await crud_articles.get_articles(skip=skip,limit=limit,keyword=keyword,db=db,author_id=author_id)
    data = [ArticleResponse.model_validate(article) for article in db_articles]
    return success_response(message="查询成功",data=data)

# 更新文章
@router.put("/update/{article_id}")
async def update_article(article_id:int,article: ArticleUpdate,
                   db:AsyncSession = Depends(get_db),
                   current_user=Depends(get_current_user)):
    db_article=await crud_articles.get_article_id(article_id=article_id,db=db)
    if db_article is None:
        raise HTTPException(status_code=404,detail="文章不存在")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403,detail="无法更改文章")
    update_article=await crud_articles.update_article(db_article=db_article,update_article=article,db=db)
    data=ArticleUpdate.model_validate(update_article)
    return success_response(message="修改成功",data=data)

# 删除文章
@router.delete("/delete/{article_id}")
async def delete_article(article_id:int,db:AsyncSession= Depends(get_db),
                   current_user=Depends(get_current_user)):
    db_article=await crud_articles.get_article_id(article_id=article_id, db=db)
    if not db_article:
        raise HTTPException(status_code=404,detail="删除文章失败")
    await crud_articles.delete_article(article_id=article_id,db=db,uer_id=current_user.id)
    return success_response(message=f"ID为{article_id}的文章删除成功")