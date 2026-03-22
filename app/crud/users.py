####################用户##########################
from sqlalchemy.orm import Session
from app.core import security
from app.core.security import get_password_hash
from app.models.users import DBUser
from app.schemas.users import UserCreate, UserUpdateRequest
from sqlalchemy import update

# 创建用户
def create_user(db:Session,user:UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user=DBUser(username=user.username,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 用户模糊搜索
def get_user_by_username(db:Session,skip:int=0,limit:int=10,keyword:str=None):
    get_user_skip=db.query(DBUser)
    if keyword:
        get_user_skip=db.query(DBUser).filter(DBUser.username.ilike(f"%{keyword}%"))
    return get_user_skip.offset(skip).limit(limit).all()

# 登录或注册时是否有同名
def get_users(db:Session,username:str):
    return db.query(DBUser).filter(DBUser.username==username).first()


# 修改个人信息
def update_user(db:Session,username:str,update_user=UserUpdateRequest):
    update_dict=update_user.model_dump(exclude_unset=True,exclude_none=True)
    if not update_dict:
        return get_users(db,username)
    query=update(DBUser).where(DBUser.username==username).values(**update_dict)
    result=db.execute(query)
    db.commit()

    if result.rowcount==0:
        return None
    return get_users(db,username)

# 修改密码
def update_password(db:Session,user:DBUser,old_password:str,new_password:str):
    if not security.verify_password(old_password,user.hashed_password):
        return False
    hash_new_password=security.get_password_hash(new_password)
    user.hashed_password=hash_new_password
    # 更新:由SQLALchemy真正接管这个User对象，确保可以commit
    # 规避 session过期或关闭导致的不能提交的问题
    db.add(user)
    db.commit()
    db.refresh(user)
    return True