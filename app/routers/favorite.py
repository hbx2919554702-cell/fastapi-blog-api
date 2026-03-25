from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.depends import get_current_user
from app.core.response import success_response
from app.crud.favorite import is_article_favorite, add_article_favorite, get_favorite_list, delete_favorite_list,delete_article_favorite
from app.database import get_db
from app.models.users import DBUser
from app.schemas.favorite import FavoriteResponse, FavoriteAddRequest, FavoriteDeleteRequest, FavoriteListResponse

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 查看收藏状态
@router.get("/check")
async def check_favorite(article_id: int=Query(...,alias="article_id"),
                         db : AsyncSession=Depends(get_db),
                         user :DBUser=Depends(get_current_user)):
    result=await is_article_favorite(db, user.id, article_id)
    return success_response(message="检擦收藏状态成功",data=FavoriteResponse(isFavorite=result))

# 添加收藏
@router.post("/add_favorite")
async def add_favorite(data:FavoriteAddRequest,
                       db : AsyncSession=Depends(get_db),
                       user :DBUser=Depends(get_current_user)):
    add= await add_article_favorite(db=db,article_id=data.article_id,user_id=user.id)
    if add is None:
        raise HTTPException(status_code=404,detail="文章不存在，无法收藏")
    return success_response(message="收藏成功",data=add)


# 删除收藏
@router.delete("/delete_favorite")
async def delete_favorite(data:FavoriteDeleteRequest,
                          db : AsyncSession=Depends(get_db),
                          user :DBUser=Depends(get_current_user)):
    delete = await delete_article_favorite(db=db, user_id=user.id, article_id=data.article_id)
    if not delete:
        raise HTTPException(status_code=404,detail="收藏记录不存在")
    return success_response(message="取消收藏成功")

# 查看收藏列表
@router.get("/list_favorite")
async def get_list_favorite(page:int=Query(1,ge=1,description="请求的页码从1开始"),
                        limit:int=Query(10,gt=1,le=20,alias="Limit",description="每页数量"),
                        db:AsyncSession=Depends(get_db),
                        user: DBUser=Depends(get_current_user)):
    total,rows=await get_favorite_list(db,user.id,page,limit)
    favorite_list=[{
        **articles.__dict__,
        "owner":{"nickname":articles.owner.nickname if articles.owner.nickname else "匿名用户"},
        "favorite_at":favorite_at,
        "favorite_id":favorite_id,
    }for articles,favorite_at,favorite_id in rows]
    has_more=total>page*limit
    data=FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功",data=data)

# 清空收藏列表
@router.delete("/list_delete")
async def get_list_delete(
                      db:AsyncSession=Depends(get_db),
                      user:DBUser=Depends(get_current_user)):
    result=await delete_favorite_list(db=db, user_id=user.id)
    return success_response(message=f"成功清除{result}条收藏记录")