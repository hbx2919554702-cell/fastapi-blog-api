from typing import List, Any, Dict, Optional

from app.core.cache_redis import get_json_cache, set_cache, delete_cached_articles

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
                              author_id: Optional[int] = None, expire:int=1800  ):
    key = generate_articles_cache_key(page, limit, keyword, author_nickname, author_id)
    return await set_cache(key,data,expire)

# 清除缓存-文章列表
async def clear_cached_articles():
    await delete_cached_articles(f"{ARTICLES_KEY}*")