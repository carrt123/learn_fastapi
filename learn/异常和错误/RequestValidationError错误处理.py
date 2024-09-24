from fastapi import Request
from fastapi import FastAPI, Query, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({'mes': '触发了RequestValidationError错误，，错误信息:%s ！' % (str(exc))})


@app.get("/request_exception/")
async def request_exception(user_id: int):
    return {"user_id": user_id}


@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    pass
    websocket.query_params


if __name__ == "__main__":
    import uvicorn
    import os

    uvicorn.run(app, host='127.1.1.1')
