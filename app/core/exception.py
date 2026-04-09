from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"系统崩溃拦截，请求路径：{request.url.path} | 错误类型:{type(exc).__name__}",
                 exc_info=True)

    return JSONResponse(status_code=500,
                        content={
                            "code":500,
                            "message":"服务器开了小差，请稍后再联系管理员",
                            "data":None
                        })