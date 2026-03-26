from fastapi import APIRouter, Depends, HTTPException,Query


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.depends import get_current_user
from app.core.response import success_response
from app.crud.history import add_history, get_list_history, delete_history_user, delete_list_history
from app.database import get_db
from app.models.users import DBUser
from app.schemas.history import HistoryListResponse

router = APIRouter(prefix="/api/history", tags=["history"])

# 添加浏览记录
@router.post("/post_history")
async def create_history(article_id: int,
                         db:AsyncSession=Depends(get_db),
                         user:DBUser = Depends(get_current_user)):
    history= await add_history(db=db,article_id=article_id, user_id=user.id)
    if history is None:
        raise HTTPException(status_code=404,detail="文章不存在，浏览记录添加失败")
    return success_response(message="添加浏览记录成功", data=history)

# 查看浏览记录
@router.get("/list_history")
async def get_history(page:int=Query(1,ge=1,description="请求的页码从1开始"),
                       limit:int=Query(10,gt=1,le=20,alias="Limit",description="每页数量"),
                       db:AsyncSession=Depends(get_db),
                       user=Depends(get_current_user)):
    rows,total=await get_list_history(db=db,page=page,limit=limit,user_id=user.id)
    history_list=[{
        **articles.__dict__,
        "history_id":history_id,
        "history_at":history_at,
        "owner":{"nickname":articles.owner.nickname if articles.owner.nickname else "匿名用户"}
    }for articles,history_id,history_at in rows]
    has_more=page*limit>total
    data=HistoryListResponse(list=history_list,total=total,hasMore=has_more)
    return success_response(message="获取浏览记录列表成功",data=data)

# 删除浏览记录
@router.delete("/delete_history")
async def delete_history(article_id:int,db:AsyncSession=Depends(get_db),
                         user:DBUser = Depends(get_current_user)):
    history= await delete_history_user(db=db,article_id=article_id,user_id=user.id)
    if history is None:
        raise HTTPException(status_code=404,detail="清除浏览记录失败")
    return success_response(message="清除浏览记录成功")


 #清除浏览记录列表
@router.delete("/delete_history_list")
async def delete_history_list(db:AsyncSession=Depends(get_db),
                              user:DBUser = Depends(get_current_user)):
    history= await delete_list_history(db=db,user_id=user.id)
    return success_response(message=f"清除{history}条浏览记录")
