from datetime import datetime
from sqlalchemy import select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.articles import DBArticle
from app.schemas.articles import ArticleUpdate ,ArticleCreate

# 根据id查询
async def get_article_id(db:AsyncSession,article_id:int):
    db_article=(select(DBArticle).options(joinedload(DBArticle.owner)).
                filter(DBArticle.id == article_id))
    result = await db.execute(db_article)
    return result.scalar_one_or_none()

# 查询全部
async def get_articles(db:AsyncSession,skip:int=0,limit:int=10,keyword:str=None,author_id:str=None):
    get_article_skip=select(DBArticle).options(joinedload(DBArticle.owner))
    # 模糊搜索
    if keyword:
        get_article_skip=get_article_skip.filter(DBArticle.title.ilike(f"%{keyword}%"))
    if author_id:
        get_article_skip=get_article_skip.filter(DBArticle.author_id==author_id)
    get_article_skip.offset(skip).limit(limit)
    result = await db.execute(get_article_skip)
    return result.scalars().unique().all()

# 写入
async def create_article(db:AsyncSession,article:ArticleCreate,author_id: int):
    db_article=DBArticle(title=article.title,content=article.content,author_id=author_id)
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    return db_article

# 删除
async def delete_article(db:AsyncSession,article_id:int,uer_id:int):
    db_article=delete(DBArticle).where(DBArticle.id==article_id,DBArticle.author_id==uer_id)
    result=await db.execute(db_article)
    await db.commit()
    return result.rowcount>0

# 更新
async def update_article(db:AsyncSession,db_article:DBArticle,update_article:ArticleUpdate):
    update_data=update_article.model_dump(exclude_unset=True,exclude_none=True)
    for key ,value in update_data.items():
        setattr(db_article,key,value)
    db_article.updated_at=datetime.now()
    await db.commit()
    await db.refresh(db_article)
    return db_article