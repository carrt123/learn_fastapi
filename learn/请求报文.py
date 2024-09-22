import enum
from typing import Optional, List

from fastapi import FastAPI, Path, Query, Request
import uvicorn

app = FastAPI(debug=True)


@app.get("/get_request")
async def get_request(request: Request):
    form_data = await request.form()
    body_data = await request.body()
    return {
        "url": request.url,
        "base_url": request.base_url,
        "client_host": request.client.host,
        "query_params": request.query_params,
        "json_data": await request.json() if body_data else None,
        "form_data": form_data,
        "body_data": body_data
    }


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
