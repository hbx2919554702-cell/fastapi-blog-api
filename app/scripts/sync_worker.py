import asyncio
from app.database import AsyncSessionLocal
from app.core.cache_redis import redis_client
from app.models.articles import DBArticle
from app.core.logger import logger
from sqlalchemy import update, bindparam


async def consume_view_count():
    set_key="pending_sync_articles"
    while True:
        try:
            pending_ids=await redis_client.smembers(set_key)
            if not pending_ids:
                await asyncio.sleep(60)
                continue

            bulk_data=[]
            valid_ids=[]

            for article_id_str in pending_ids:
                article_id=int(article_id_str)
                key=f"article_view_incr_{article_id}"
                incr_str=await redis_client.get(key)

                if incr_str:
                    bulk_data.append({
                        "b_id":article_id,
                        "b_incr":int(incr_str)
                        })
                    valid_ids.append(article_id_str)
                else:
                    await redis_client.srem(set_key, article_id)

            if bulk_data:
                async with AsyncSessionLocal() as db:
                    stmt=(update(DBArticle).where(DBArticle.id==bindparam("b_id")).
                            values(view_count=DBArticle.view_count+bindparam("b_incr"))
                        )
                    await db.execute(stmt,bulk_data)
                    await db.commit()


                # 如果 MySQL 挂了抛异常，代码根本走不到这里，Redis 数据得以保留！
                async with redis_client.pipeline(transaction=True) as pipe:
                    for aid in valid_ids:
                        pipe.delete(f"article_view_incr_{aid}")
                        pipe.srem(set_key, aid)
                    await pipe.execute()
                logger.info(f"成功将{len(bulk_data)}篇文章的浏览量写入数据库。")
        except Exception as e:
            logger.error(f"落盘崩溃，redis数据库未丢。等待重试{e}")
        await asyncio.sleep(300)

if __name__ == '__main__':
    asyncio.run(consume_view_count())