from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field

#######################文章#####################
# 增
class ArticleCreate(BaseModel):
    title: str=Field(min_length=2,max_length=15,description="文章名要求2到15个字符")
    content: str
    author: str

# 查所有文章
class ArticleResponse(ArticleCreate):
    id:int
    created_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None
    class Config:
        from_attributes = True

# 根据文章id查文章
class ArticleDetail(ArticleCreate):
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        from_attributes = True

# 更新
class ArticleUpdate(ArticleCreate):
    pass



#################### 用户类######################
#创建用户
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