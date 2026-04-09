from fastapi import Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.users import get_users
from app.database import get_db
from app.core.cache_redis import redis_client
# 封装获取Token到查询用户的工具函数(登录校验依赖)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/users/login" )
async def get_current_user(token: str = Depends(oauth2_scheme),
                     db: AsyncSession=Depends(get_db)):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的凭证(Token里没有用户名)")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期,请重新登录"
        )
    user=await get_users(db=db,username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token验证成功，但无法找到该用户(可能已经被删除)"
    )
    return user



# 可选登录依赖
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/users/login", auto_error=False)
async def get_current_user_optional(
        token: str | None = Depends(oauth2_scheme_optional),
        db: AsyncSession = Depends(get_db)
):
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    user = await get_users(db=db, username=username)
    if user is None:
        return None
    return user

# 窗口限流器
async def rate_limit(request: Request):
    client_ip=request.client.host
    path = request.url.path
    key=f"rate_limit_{client_ip}_{path}"

    max_request=30
    window_seconds=60

    try:
        current_count= await redis_client.incr(key)
        if current_count==1:
            await redis_client.expire(key, window_seconds)
        if current_count > max_request:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="您的操作过于频繁，请稍后再试"
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"限流中间件 Redis 异常，执行降级放行: {e}")
