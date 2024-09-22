import enum
from typing import Optional, List

from fastapi import FastAPI, Path, Query
import uvicorn

app = FastAPI(debug=True)


@app.get("/query")
async def query(uid: str, name: Optional[str] = None, token: str = 'token'):
    return {'uid': uid, 'name': name, 'token': token}


@app.get("/query/bool")
async def query_booK(isbook: bool = False):
    return {'isbook': isbook}


@app.get("/query/morequery")
async def callback(
        user_id: int = Query(ge=10, le=100),
        user_name: str = Query(None, min_length=5, max_length=15),
        user_token: str = Query('token', min_length=10, max_length=30),
):
    return {'user_id': user_id, 'user_name': user_name, 'user_token': user_token}


@app.get("/query/list")
async def query_list(q: List[str] = Query(['q1', 'q2'])):

    return {'q': q}

if __name__ == '__main__':
    uvicorn.run(app, host="127.1.1.1", port=8000)
