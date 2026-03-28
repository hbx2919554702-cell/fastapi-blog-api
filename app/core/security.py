from datetime import datetime,timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 创建密码上下文
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

# 登陆时，验证密码
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

# 注册时，加密明文密码
def get_password_hash(password:str) ->str:
    return pwd_context.hash(password)

# 创建JWT Token，根据用户ID生成一串Token
def create_access_token(data:dict,expires_delta:Optional[timedelta]=None)->str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt