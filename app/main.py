from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses  import RedirectResponse
from app.routers import articles,users,favorite
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

app.include_router(articles.router)
app.include_router(users.router)
app.include_router(favorite.router)