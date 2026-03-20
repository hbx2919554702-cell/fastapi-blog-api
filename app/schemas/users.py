#################### 用户类######################
#创建用户
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str=Field(min_length=2,max_length=50,description="用户名要求3到50个字符")
    password: str=Field(max_length=6,description="密码至少6位")
    email: Optional[str]=None

# 返回
class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]=None
    class Config:
        from_attributes = True

# 返回Token
class Token(BaseModel):
    access_token: str
    token_type: str
    message: str="登陆成功"