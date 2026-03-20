from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.database import get_db
from app.schemas.users import UserResponse, UserCreate, Token, UserAuthResponse, UserInfoResponse
from app.crud.users import get_users, create_user, get_user_by_username
from app.core.security import verify_password,create_access_token
router = APIRouter(prefix="/api/users", tags=["users"])

# 用户注册
@router.post("/register")
def register_user(user:UserCreate, db:Session=Depends(get_db)):
    db_register_user=get_users(db=db,username=user.username)
    if db_register_user:
        raise HTTPException(status_code=400,detail="已存在相同用户名")
    user=create_user(db=db,user=user)
    token = create_access_token(data={"sub": user.username})
    response_data=UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)


# 登录
@router.post("/login",response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=get_users(db=db,username=form_data.username)
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="用户密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,
            "token_type": "bearer",
            "message":"登陆成功！"}

# 查找用户
@router.get('/Users',response_model=List[UserResponse])
def read_users(
               limit:int=Query(10,ge=1,le=20,description="每页数量"),
               page:int=Query(1,ge=1,description="从第一页开始"),
               keyword:Optional[str]=Query(None,description="搜索作者关键字"),
               db:Session = Depends(get_db)
):
    skip=(page-1)*limit
    user=get_user_by_username(db=db,limit=limit,skip=skip,keyword=keyword)
    if user is None:
        raise HTTPException(status_code=404,detail="作者不存在")
    return user