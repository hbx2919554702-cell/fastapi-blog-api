from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses  import RedirectResponse

from .schemas import ArticleCreate, ArticleResponse, ArticleDetail, ArticleUpdate
from .database import engine,Base,get_db
from . import crud

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端地址访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法(GET, POST, DELETE等)
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

# 写入数据
@app.post('/article',response_model=ArticleResponse)
def create_article(article:ArticleCreate,db:Session = Depends(get_db)):
    return crud.create_article(db=db,article=article)


# 读取数据
@app.get('/article',response_model=List[ArticleResponse])
def read_articles(
        db:Session = Depends(get_db),
        page:int=Query(1,description="请求的页码从1开始",ge=1),
        limit:int=Query(10,ge=1,le=100,description="每页数量"),
        keyword:Optional[str]=Query(None,description="搜索文章标题关键字")
):
    skip=(page-1)*limit
    articles=crud.get_articles(db=db,skip=skip,limit=limit,keyword=keyword)
    return articles

# 根据id读数据
@app.get('/article/{article_id}',response_model=ArticleDetail)
def read_article(article_id:int,db:Session = Depends(get_db)):
    db_article_id=crud.get_article_id(db=db,article_id=article_id)
    if db_article_id is None:
        raise HTTPException(status_code=404,detail='文章不存在')
    return db_article_id

# 删除
@app.delete('/article/{article_id}')
def delete_article(article_id:int,db:Session = Depends(get_db)):
    success=crud.delete_article(db=db,article_id=article_id)
    if success is None:
        raise HTTPException(status_code=404,detail="文章不存在")
    return {"message:",f"ID为{article_id}的文章删除成功"}

# 更新
@app.put('/article/{article_id}',response_model=ArticleUpdate)
def update_article(article_id:int,article:ArticleUpdate,db:Session = Depends(get_db)):
    db_update_article=crud.update_article(db=db,article_id=article_id,article=article)
    if db_update_article is None:
        raise HTTPException(status_code=404,detail="文章不存在")
    return db_update_article



