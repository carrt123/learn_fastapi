class Config:
    CELERY_BROKER_URL = "pyamqp://guest:guest@localhost//"  # RabbitMQ
    CELERY_RESULT_BACKEND = "rpc://"
