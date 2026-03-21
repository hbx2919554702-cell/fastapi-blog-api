#################### 用户类######################
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

#创建用户
class UserCreate(BaseModel):
    username: str=Field(min_length=2,max_length=50,description="用户名要求3到50个字符",json_schema_extra={"example": ""})
    password: str=Field(max_length=6,description="密码至少6位",json_schema_extra={"example": ""})

# 返回
class UserResponse(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(
        populate_by_name=True,  # alise 字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

# 返回Token
class Token(BaseModel):
    access_token: str
    token_type: str
    message: str="登陆成功"

# user_info的基础类
class UserInfoBase(BaseModel):
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="简洁")
    email:Optional[str]=Field(None,max_length=255,description="邮箱")

#user_info对应的类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

#data数据类型
class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field(...,alias="userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 用户更新个人信息
class UserUpdateRequest(BaseModel):
     nickname: str=None
     gender: str=None
     bio: str=None
     email: str=None

# 修改密码
class UserPassword(BaseModel):
    old_password: str=Field(...,alias="oldPassword",description="旧密码")
    new_password: str=Field(...,min_length=6,alias="newPassword",description="新密码")