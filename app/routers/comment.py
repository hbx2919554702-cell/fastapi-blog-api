from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.depends import get_current_user
from app.core.response import success_response
from app.crud.comment import add_comment, get_comment_list, delete_user_comment, delete_article_comment
from app.database import get_db
from app.models.users import DBUser
from app.schemas.comment import AddComment, CommentArticleResponse, CommentListResponse

router = APIRouter(prefix="/api/comment", tags=["comment"])

# 发表评论
@router.post("/put_comment")
async def put_comment( data:AddComment,
                       db: AsyncSession = Depends(get_db),
                       user:DBUser = Depends(get_current_user)):
    new_comment= await add_comment(db=db, user_id=user.id, article_id=data.article_id, comment=data.comment)
    if not new_comment:
        raise HTTPException(status_code=404, detail="没有找到该文章")
    response_data = CommentArticleResponse(
        id=new_comment.id,
        article_id=new_comment.article_id,
        content=new_comment.comment,
        created_at=new_comment.created_at,
        user_id=user.id,
        nickname=user.nickname
    )
    return success_response(message="评论发表成功", data=response_data.model_dump())


# 查看评论
@router.get("/get_comment")
async def get_comment(article_id: int,
                      page:int=Query(1,ge=1,description="请求的页码从1开始"),
                      limit:int=Query(10,gt=1,le=20,alias="Limit",description="每页数量"),
                      db: AsyncSession = Depends(get_db),):
     rows,total= await get_comment_list(db=db,article_id=article_id,page=page,limit=limit)
     comment_list=[{
            "id": comments.id,
           "article_id": comments.article_id,
            "comment": comments.comment,
            "created_at": comments.created_at,
            "user_id": comments.user_id,
            "user": {"nickname": comments.user.nickname if comments.user.nickname else "匿名用户"},
     }for comments  in rows]
     has_more = total > page * limit
     data=CommentListResponse(list=comment_list,total=total,hasMore=has_more)
     return success_response(message="查看评论成功", data=data)

# 删除个人聊天记录
@router.delete("/delete_comments_user")
async def delete_comments_user(comment_id: int,
                          db: AsyncSession = Depends(get_db),
                          user: DBUser = Depends(get_current_user)):
    delete=await delete_user_comment(db=db,user_id=user.id,comment_id=comment_id)
    if  not delete:
        raise HTTPException(status_code=404,detail="删除失败")
    return success_response(message="成功删除该评论")


# 文章作者删除相关文章的评论
@router.delete("/delete_comments_article")
async def delete_comments_article(comment_id: int,
                                  db: AsyncSession = Depends(get_db),
                                  user: DBUser = Depends(get_current_user)):
    result = await delete_article_comment(db=db,user_id=user.id,comment_id=comment_id)
    if not result:
        raise HTTPException(status_code=401,detail="你无法删除该评论")
    return success_response(message="成功删除该评论")