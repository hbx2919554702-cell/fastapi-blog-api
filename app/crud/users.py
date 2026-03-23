####################用户##########################
from app.core import security
from app.core.security import get_password_hash
from app.models.users import DBUser
from app.schemas.users import UserCreate, UserUpdateRequest
from sqlalchemy import update
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 创建用户
async def create_user(db:AsyncSession,user:UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user=DBUser(username=user.username,hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 用户模糊搜索
async def get_user_by_nickname(db:AsyncSession,skip:int=0,limit:int=10,keyword:str=None):
    get_user_skip=select(DBUser)
    if keyword:
        get_user_skip=select(DBUser).filter(DBUser.nickname.ilike(f"%{keyword}%"))
    get_user_skip=get_user_skip.offset(skip).limit(limit)
    result=await db.execute(get_user_skip)
    return result.scalars().all()

# 登录或注册时是否有同名
async def get_users(db:AsyncSession,username:str):
    db_user=select(DBUser).filter(DBUser.username==username)
    result=await db.execute(db_user)
    return result.scalar_one_or_none()

# 修改个人信息
async def update_user(db:AsyncSession,username:str,update_user=UserUpdateRequest):
    update_dict=update_user.model_dump(exclude_unset=True,exclude_none=True)
    if not update_dict:
        return await get_users(db,username)
    query=update(DBUser).where(DBUser.username==username).values(**update_dict)
    result=db.execute(query)
    await db.commit()

    if result.rowcount==0:
        return None
    return await get_users(db,username)

# 修改密码
async def update_password(db:AsyncSession,user:DBUser,old_password:str,new_password:str):
    if not security.verify_password(old_password,user.hashed_password):
        return False
    hash_new_password=security.get_password_hash(new_password)
    user.hashed_password=hash_new_password
    # 更新:由SQLALchemy真正接管这个User对象，确保可以commit
    # 规避 session过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True