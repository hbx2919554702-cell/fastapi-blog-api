from datetime import datetime
from sqlalchemy.orm import  Session
from .models import DBArticle
from .schemas import ArticleCreate, ArticleUpdate


# 根据id查询
def get_article_id(db:Session,article_id:int):
   return db.query(DBArticle).filter(DBArticle.id==article_id).first()

# 查询全部
def get_articles(db:Session,skip:int=0,limit:int=10,keyword:str=None):
    get_article_skip=db.query(DBArticle)
    # 模糊搜索
    if keyword:
        get_article_skip=db.query(DBArticle).filter(DBArticle.title.ilike(f"%{keyword}%"))
    return get_article_skip.offset(skip).limit(limit).all()

# 写入
def create_article(db:Session,article:ArticleCreate):
    db_article=DBArticle(title=article.title,content=article.content,author=article.author)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

# 删除
def delete_article(db:Session,article_id:int):
    db_article=db.query(DBArticle).filter(DBArticle.id==article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False

# 更新
def update_article(db:Session,article_id:int,article:ArticleUpdate):
    db_article=db.query(DBArticle).filter(DBArticle.id==article_id).first()
    if db_article:
        db_article.title=article.title
        db_article.content=article.content
        db_article.author=article.author
        db_article.updated_at=datetime.now()

        db.commit()
        db.refresh(db_article)
        return db_article
    return  None