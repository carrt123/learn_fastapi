import enum

from fastapi import FastAPI, Path
import uvicorn

app = FastAPI(debug=True, reload=True)


# 必须参数
@app.get("/user/{user_id}/article/{article_id}")
async def get_user_article(user_id: int, article_id: int):
    return {"user_id": user_id, "article_id": article_id}


# 带"/"参数
@app.get("/uls/{file_path:path}")
async def get_file(file_path: str=Path(..., title="文件路径", description='文件路径信息')):
    return {"file_path": file_path}


class bookName(str, enum.Enum):
    python = "python"
    java = "java"


# 枚举类型参数
@app.get("/book/{book_name}")
async def get_book(book_name: bookName = Path(..., title="书籍名称", description='书籍名称信息')):
    return {"book_name": book_name}


@app.get("/pay/{user_id}/article/{article_id}")
async def callback(user_id: int = Path(..., title="用户ID", description='用户ID信息', ge=10000),
                   article_id: str = Path(..., title="文章ID", description='用户所属文章ID信息', min_length=1,
                                          max_length=50)):
    return {
        'user_id': user_id,
        'article_id': article_id
    }


if __name__ == '__main__':
    uvicorn.run(app, host="127.1.1.1", port=8000)
