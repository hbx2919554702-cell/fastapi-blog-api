from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.depends import get_current_user, get_current_user_optional
from app.core.response import success_response
from app.crud.history import add_history
from app.database import get_db
from app.schemas.articles import ArticleCreate, ArticleUpdate, ArticleDetail, ArticleShow
from app.crud import articles as crud_articles
from fastapi import BackgroundTasks
from app.cache.articles import incr_article_view, delayed_sync_view_count

router = APIRouter(prefix="/api/articles", tags=["articles"])

# 创建文章
@router.post("/create")
async def create_article(article:ArticleCreate,
                   db:AsyncSession= Depends(get_db),
                   current_user=Depends(get_current_user)):
    data= await crud_articles.create_article(db=db,article=article,author_id=current_user.id)
    safe_data = ArticleShow.model_validate(data).model_dump()
    return success_response(message="创建成功",data=safe_data)

# 根据id搜索文章
@router.get("/get_articles_id/{article_id}")
async def get_articles_id(article_id:int,
                          background_tasks:BackgroundTasks,
                          db:AsyncSession = Depends(get_db),
                          current_user=Depends(get_current_user_optional)):
    db_article_id = await crud_articles.get_article_id(article_id=article_id,db=db)
    if db_article_id is None:
        raise HTTPException(status_code=404,detail='文章不存在')
    # 将cache层任务丢给后台
    current_incr=await incr_article_view(article_id=article_id)
    if current_incr ==1:
        background_tasks.add_task(delayed_sync_view_count,article_id,delay_seconds=300)
    data=ArticleDetail.model_validate(db_article_id)
    # 视图合并
    data.view_count+=current_incr
    if current_user:
        await add_history(db=db,article_id=article_id,user_id=current_user.id)
    return success_response(message="查询成功",data=data)


# 模糊搜索
@router.get("/get_articles")
async def get_articles(page:int=Query(1,ge=1,description="请求的页码从1开始"),
                 limit:int=Query(10,gt=1,le=20,description="每页数量"),
                 keyword:Optional[str]=Query(None,description="搜索文章标题关键字"),
                 author_nickname: Optional[str] = Query(None, description="搜索作者昵称"),
                 author_id: Optional[int] =Query(None,escription="搜索作者昵ID"),
                 db:AsyncSession = Depends(get_db)):
    db_articles = await crud_articles.get_articles(page=page,limit=limit,keyword=keyword,db=db,author_nickname=author_nickname,author_id=author_id)
    data = [article.model_dump() for article in db_articles]
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
    data = ArticleShow.model_validate(update_article).model_dump()
    return success_response(message="修改成功",data=data)

# 删除文章
@router.delete("/delete/{article_id}")
async def delete_article(article_id:int,db:AsyncSession= Depends(get_db),
                   current_user=Depends(get_current_user)):
    db_article = await crud_articles.get_article_id(article_id=article_id, db=db)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")

    delete_result = await crud_articles.delete_article(db=db, article_id=article_id, uer_id=current_user.id)
    if not delete_result:
        raise HTTPException(status_code=403, detail="越权操作：你无权删除他人的文章！")
    return success_response(message=f"ID为{article_id}的文章删除成功")