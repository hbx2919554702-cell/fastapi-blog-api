import asyncio
from typing import List, Any, Dict, Optional
import random
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache_redis import get_json_cache, set_cache,delete_cached, redis_client
from app.core.logger import logger
from app.models.articles import DBArticle
from sqlalchemy import update

ARTICLES_KEY = "articles_list:"

def generate_articles_cache_key(page: int,limit: int,
                                keyword: Optional[str] = None,
                                author_nickname: Optional[str] = None,
                                author_id: Optional[int] = None) -> str:

    kw = keyword if keyword else "all"
    nick = author_nickname if author_nickname else "all"
    aid = author_id if author_id else "all"
    return f"{ARTICLES_KEY}:page:{page}:limit:{limit}:kw:{kw}:nick:{nick}:aid:{aid}"


# 获取缓存-文章列表
async def get_cached_articles(page:int,limit:int,keyword: Optional[str] = None,
    author_nickname: Optional[str] = None,
    author_id: Optional[int] = None):
    key=generate_articles_cache_key(page, limit, keyword, author_nickname, author_id)
    return await get_json_cache(key)

# 写入缓存-文章列表
async def set_cached_articles(page:int,limit:int,data:List[Dict[str, Any]],
                              keyword: Optional[str] = None,
                              author_nickname: Optional[str] = None,
                              author_id: Optional[int] = None, expire:int=60+random.randint(0,60 ) ):
    key = generate_articles_cache_key(page, limit, keyword, author_nickname, author_id)
    return await set_cache(key,data,expire)

# 清除缓存-文章列表
async def clear_cached_articles():
    await delete_cached(f"{ARTICLES_KEY}*")


# 增加浏览量缓存
async def incr_article_view(article_id:int):
    key=f"article_view_incr_{article_id}"
    try:
        return await redis_client.incr(key)
    except Exception as e:
        logger.error(f"Redis浏览量incr失败{e}")
        return 0


# 延迟将浏览增量写入数据库
async def delayed_sync_view_count(article_id:int,delay_seconds:int=300):
    await asyncio.sleep(delay_seconds)
    key = f"article_view_incr_{article_id}"

    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.get(key)
        pipe.delete(key)
        result=await pipe.execute()

    incr_value=result[0]
    if incr_value and incr_value > 0:
        total_incr=int(incr_value)
        async with AsyncSession() as db:
            stmt=update(DBArticle).where(DBArticle.id==article_id).values(view_count=DBArticle.view_count+total_incr)
            await db.execute(stmt)
            await db.commit()