import asyncio
from logging.config import fileConfig
import sys
import os

#路径追加必须放在最前面，确保能找到 app 目
sys.path.append(os.getcwd())

from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
# 触发 __init__.py，一次性把所有模型都加载并注册到 Base.metadata
from app.models.articles import DBArticle
from app.models.users import DBUser
from app.models.favorite import Favorite
from app.models.comment import Comment
from app.models.history import History
from app.database import Base

sys.path.append(os.getcwd())
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url =settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """这是一个同步包装函数，用来给下面的 run_sync 调用"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    """真正的全异步执行逻辑"""
    # 从配置创建异步引擎，迁移时建议使用 NullPool 避免连接冲突
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # 在异步连接中安全地运行同步的迁移逻辑
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 用 asyncio 启动异步函数
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
