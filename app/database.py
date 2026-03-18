import os
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base


# 1. 配置数据库地址：这就相当于你的 SQL Server 连接字符串
# sqlite:///./blog.db 意思是：在当前目录下，给我建一个名叫 blog.db 的文件当数据库
current_dir = os.path.dirname(os.path.abspath(__file__))   #获取当前文件路径
root_dir = os.path.dirname(current_dir)                   #获得上一级目录路径
DB_PATH = os.path.join(root_dir, "blog.db")               #找到该路径的blog.db文件
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"        #连接blog数据库

# 创建和数据库沟通的引擎，解决并发冲突
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

# 关闭自动确认和自动更新，绑定engine引擎
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

# 创建基础类
Base=declarative_base()

# 定义一个获取数据库连接的生成器，这是 Depends 的核心
def get_db():
    db=SessionLocal()
    try:
        yield db       #借接口
    finally:
        db.close()