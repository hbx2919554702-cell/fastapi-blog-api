import json
from typing import Any
import redis.asyncio as redis
from app.core.config import settings

redis_client=redis.Redis(host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True)

# 读字符串
async  def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存{e}失败")
        return None

# 读字典或列表
async def get_json_cache(key:str):
    try:
        date=await redis_client.get(key)
        if date:
            return json.loads(date) #序列化
    except Exception as e:
        print(f"获取JSON缓存{e}失败")
        return None

# 设置缓存
async def set_cache(key:str,value=Any,expire:int=3600):
    try:
        if isinstance(value, (dict, list)):
            value=json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存{e}失败")
        return False

# 清除缓存
async def delete_cached_articles(pattern:str):
    try:
        cursor="0"
        while cursor!=0:
            cursor,key=await redis_client.scan(cursor=cursor,match=pattern,count=100)
            if key:
                await redis_client.delete(*key)
            return True
    except Exception as e:
        print(f"批量删除缓存失败:{e}")
        return False
