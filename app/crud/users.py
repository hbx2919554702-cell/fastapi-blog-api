####################用户##########################
# 创建用户
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.users import DBUser
from app.schemas.users import UserCreate

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