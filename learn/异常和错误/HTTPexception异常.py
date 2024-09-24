import asyncio

from fastapi import Request
from fastapi import FastAPI, Query, HTTPException
from starlette.responses import JSONResponse

# 需要注意设置使用的事件循环方式
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()


# 自定义异常, 异常被处理成我们想要的格式
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)


@app.get("/http_exception")
async def http_exception(action_scopes: str = Query(default='admin')):
    if action_scopes == 'admin':
        raise HTTPException(status_code=403,
                            headers={"x-auth": "NO AUTH!"},
                            detail={
                                'code': '403',
                                'message': '错误当前你没有权限访问',
                            })
    return {'code': '200', }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=9082)
