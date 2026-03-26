from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.articles import DBArticle
from app.models.favorite import Favorite


# 检查用户是否收藏该文章
async def is_article_favorite(db: AsyncSession, user_id:int, article_id: int):
    query=select(Favorite).where(Favorite.user_id==user_id, Favorite.article_id==article_id)
    result = await db.execute(query)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None


# 用户添加收藏文章
async def add_article_favorite(db: AsyncSession,user_id: int,article_id:int):
    result=await db.execute(select(DBArticle).where(DBArticle.id==article_id))
    article=result.scalar_one_or_none()
    if not article:
        return None
    favorite= Favorite(user_id=user_id, article_id=article_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 删除收藏文章
async def delete_article_favorite(db: AsyncSession, user_id:int, article_id:int):
    favorite = delete(Favorite).where(Favorite.user_id==user_id, Favorite.article_id==article_id)
    result = await db.execute(favorite)
    await db.commit()
    return result.rowcount>0


# 查看收藏列表
async def get_favorite_list(db:AsyncSession, user_id:int, page:int=1, limit:int=10):
    # 查看收藏总数
    count_query=select(func.count()).where(Favorite.user_id==user_id)
    count_result = await db.execute(count_query)
    total=count_result.scalar_one_or_none()

    # 查找收藏
    skip=(page-1)*limit
    query=(select(DBArticle,Favorite.created_at.label("favorite_at"),Favorite.id.label("favorite_id"))
           .join(Favorite,Favorite.article_id==DBArticle.id)
           .options(joinedload(DBArticle.owner))
           .where(Favorite.user_id==user_id)
           .order_by(Favorite.created_at.desc())
           .offset(skip).limit(limit))
    result = await db.execute(query)
    rows=result.all()
    return total,rows


# 清除收藏列表
async def delete_favorite_list (db:AsyncSession, user_id:int):
    favorite=delete(Favorite).where(Favorite.user_id==user_id)
    result = await db.execute(favorite)
    await db.commit()
    return result.rowcount or 0