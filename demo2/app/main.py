from fastapi import FastAPI, BackgroundTasks
from tasks import send_notification

app = FastAPI()


@app.post("/notify/")
async def notify(email: str, message: str):
    """
    处理预约通知的请求
    """
    # 异步触发 Celery 任务
    task = send_notification.delay(email, message)
    return {"message": "Notification task created.", "task_id": task.id}


@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    获取任务状态
    """
    result = send_notification.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}
