from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.articles import DBArticle
from app.models.users import DBUser
from app.schemas.articles import ArticleUpdate ,ArticleCreate
from app.models.comment import Comment
from app.models.favorite import Favorite
from app.models.history import History

# 根据id查询
async def get_article_id(db:AsyncSession,article_id:int):
    db_article=(select(DBArticle).options(joinedload(DBArticle.owner)).
                where(DBArticle.id == article_id))
    result = await db.execute(db_article)
    article = result.scalar_one_or_none()

    if not article:
        return None
    stmt = (update(DBArticle).where(DBArticle.id == article_id).values(view_count=DBArticle.view_count + 1))
    await db.execute(stmt)
    await db.commit()
    await db.refresh(article)
    return article

# 查询全部
async def get_articles(db:AsyncSession,skip:int=0,limit:int=10,keyword:str=None,author_nickname: str = None):
    get_article_skip = select(DBArticle).join(DBArticle.owner).options(joinedload(DBArticle.owner))
    # 模糊搜索
    if keyword:
        get_article_skip=get_article_skip.where(DBArticle.title.ilike(f"%{keyword}%"))
    if author_nickname:
        get_article_skip = get_article_skip.where(DBUser.nickname.ilike(f"%{author_nickname}%"))
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
    query = select(DBArticle).where(DBArticle.id == article_id, DBArticle.author_id == uer_id)
    result = await db.execute(query)
    article = result.scalar_one_or_none()

    if not article:
        return False

    await db.execute(delete(Comment).where(Comment.article_id == article_id))
    await db.execute(delete(Favorite).where(Favorite.article_id == article_id))
    await db.execute(delete(History).where(History.article_id == article_id))

    await db.delete(article)
    await db.commit()
    return True

# 更新
async def update_article(db:AsyncSession,db_article:DBArticle,update_article:ArticleUpdate):
    update_data=update_article.model_dump(exclude_unset=True,exclude_none=True)
    for key ,value in update_data.items():
        setattr(db_article,key,value)
    db_article.updated_at=func.now()
    await db.commit()
    await db.refresh(db_article)
    return db_article