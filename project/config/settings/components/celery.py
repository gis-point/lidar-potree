from decouple import config


CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", cast=str)
CELERY_RESULT_BACKEND: str = config("CELERY_RESULT_BACKEND", cast=str)
CELERY_TASK_SERIALIZER: str = "json"
CELERY_RESULT_SERIALIZER: str = "json"
CELERY_ACKS_LATE: bool = True
CELERY_PREFETCH_MULTIPLIER: int = 1
CELERY_ACCEPT_CONTENT: list[str] = ["application/json"]
CELERY_TASK_RESULT_EXPIRES: int = 10 * 60
CELERY_TASK_TIME_LIMIT: int = 8 * 60 * 60  # 8 hours
CELERY_TASK_SOFT_TIME_LIMIT: int = 10 * 60 * 60  # 10 hours
