from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.response import success_response
from app.database import get_db
from app.models.users import DBUser
from app.schemas.users import UserResponse, UserCreate, Token, UserAuthResponse, UserInfoResponse, UserUpdateRequest, \
    UserPassword
from app.crud.users import get_users, create_user, update_user, update_password, \
    get_user_by_nickname
from app.core.security import verify_password,create_access_token
from app.core.depends import get_current_user
router = APIRouter(prefix="/api/users", tags=["users"])

# 用户注册
@router.post("/register")
async def register_user(user:UserCreate, db:AsyncSession=Depends(get_db)):
    db_register_user= await get_users(db=db,username=user.username)
    if db_register_user:
        raise HTTPException(status_code=400,detail="已存在相同用户名")
    new_user=await create_user(db=db,user=user)
    token = create_access_token(data={"sub": new_user.username})
    response_data=UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(new_user))
    return success_response(message="注册成功",data=response_data)


# 登录
@router.post("/login",response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession=Depends(get_db)):
    user=await get_users(db=db,username=form_data.username)
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="用户密码错误")
    # 登录以后拿到一个新token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,
            "token_type": "bearer",
            "message":"登陆成功！"}

# 查找用户
@router.get('/Users',response_model=List[UserResponse])
async def read_users(
               limit:int=Query(10,ge=1,le=20,description="每页数量"),
               page:int=Query(1,ge=1,description="从第一页开始"),
               keyword:Optional[str]=Query(None,description="搜索作者关键字"),
               db:AsyncSession = Depends(get_db)
):
    skip=(page-1)*limit
    user=await get_user_by_nickname(db=db,limit=limit,skip=skip,keyword=keyword)
    if user is None:
        raise HTTPException(status_code=404,detail="作者不存在")
    return user

# 获取个人信息
@router.get('/info',response_model=UserInfoResponse)
async def get_user_info(current_user: DBUser=Depends(get_current_user)):
    user_info=UserInfoResponse.model_validate(current_user)
    return success_response(message="获取用户信息成功！",data=user_info)

# 更改个人信息
@router.put('/update',response_model=UserInfoResponse)
async def update_user_info(user_data:UserUpdateRequest,current_user: DBUser=Depends(get_current_user),
                     db:AsyncSession=Depends(get_db)):
    updated_user=await update_user(username=current_user.username,update_user=user_data,db=db)
    if updated_user is None:
        raise HTTPException(status_code=404,detail="用户更新失败")
    user_info=UserInfoResponse.model_validate(updated_user)
    return success_response(message="个人信息更新成功",data=user_info)

# 更改密码
@router.put('/password',response_model=UserPassword)
async def update_user_password(password:UserPassword,current_user: DBUser=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):
    updated_password=await update_password(new_password=password.new_password,old_password=password.old_password,user=current_user,db=db)
    if not updated_password:
        raise HTTPException(status_code=500,detail="旧密码错误")
    return success_response(message="密码修改成功")