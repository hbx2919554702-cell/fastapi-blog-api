import json
from typing import Any

import redis.asyncio as redis

redis_client=redis.Redis(host="127.0.0.1",
            port=6379,
            db=0,
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