from sqlalchemy import select, func,delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.articles import DBArticle
from app.models.history import History


# 添加浏览记录
async def add_history(db:AsyncSession,article_id: int,user_id: int):
    article_query = await db.execute(select(DBArticle).where(DBArticle.id == article_id))
    article = article_query.scalar_one_or_none()
    if not article:
        return None

    query=await db.execute(select(History).where(History.user_id == user_id,History.article_id==article_id))
    update_history=query.scalar_one_or_none()
    if  update_history :
        update_history.viewed_at=func.now()
        await db.commit()
        await db.refresh(update_history)
        return update_history
    else:
        new_history=History(article_id=article_id,user_id=user_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        return new_history

# 查看浏览历史
async def get_list_history(db:AsyncSession,user_id: int,page:int=1,limit:int=10):
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one_or_none()

    skip = (page-1)*limit
    get=(select(DBArticle,History.id.label("history_id"),History.viewed_at.label("history_at"))
         .join(History,History.article_id==DBArticle.id)
         .options(joinedload(DBArticle.owner))
         .where(History.user_id == user_id)
         .order_by(History.viewed_at.desc())
         .offset(skip).limit(limit))
    result = await db.execute(get)
    rows=result.all()
    return rows,total

# 删除浏览记录(单条)
async def delete_history_user(db:AsyncSession,article_id:int,user_id:int):
    history=delete(History).where(History.article_id==article_id,History.user_id == user_id)
    result = await db.execute(history)
    await db.commit()
    return result.rowcount>0

async def delete_list_history(db:AsyncSession,user_id:int):
    history=delete(History).where(History.user_id == user_id)
    result = await db.execute(history)
    await db.commit()
    return result.rowcount or 0