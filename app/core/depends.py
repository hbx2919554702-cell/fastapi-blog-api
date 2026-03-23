# 封装获取Token到查询用户的工具函数(登录校验依赖)
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import get_users
from app.database import get_db
from app.core.config import SECRET_KEY,ALGORITHM
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/users/login")
async def get_current_user(token: str = Depends(oauth2_scheme),
                     db: AsyncSession=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
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


