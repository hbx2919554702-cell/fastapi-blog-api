from sqlalchemy import select, func,delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.articles import DBArticle
from app.models.comment import Comment

# 发表评论
async def add_comment(db:AsyncSession, user_id:int,article_id: int,comment:str):
    result = await db.execute(select(DBArticle).where(DBArticle.id == article_id))
    article = result.scalar_one_or_none()
    # 查找发表评论的文章是否存在
    if not article:
        return None
    new_comment=Comment(user_id=user_id, article_id=article_id, comment=comment)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

# 查看评论
async def get_comment_list(db:AsyncSession,article_id:int,page:int=1,limit:int=20):
    # 查看评论总数
    count_query = select(func.count()).where(Comment.article_id == article_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one_or_none()

    skip = (page-1)*limit
    get=(select(Comment).options(joinedload(Comment.user))
         .where(Comment.article_id==article_id)
         .order_by(Comment.created_at.desc())
         .limit(limit)
         .offset(skip))
    result=await db.execute(get)
    rows=result.scalars().all()
    return rows,total

# 删除个人评论
async def delete_user_comment(db:AsyncSession,user_id:int,comment_id:int):
    comment = delete(Comment).where(Comment.id == comment_id,Comment.user_id == user_id)
    result = await db.execute(comment)
    await db.commit()
    return result.rowcount>0




# 文章作者删除相关文章的评论
async def delete_article_comment(db:AsyncSession,user_id:int,comment_id:int):
   subq=select(DBArticle.id).where(DBArticle.author_id == user_id)
   comment=delete(Comment).where(Comment.id == comment_id,Comment.article_id.in_(subq))
   result = await db.execute(comment)
   await db.commit()
   return result.rowcount>0



