from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi.responses  import RedirectResponse

from app.core.depends import rate_limit
from app.routers import articles, users, favorite, comment,history
from app.core.exception import global_exception_handler

# 限流依赖
app = FastAPI(dependencies=[Depends(rate_limit)])

# 全局异常处理
app.add_exception_handler(Exception, global_exception_handler)

# 跨域中间件
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


app.include_router(articles.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(comment.router)
app.include_router(history.router)