# flask config
CELERY=dict(
    broker_url="redis://127.0.0.1",
        result_backend="redis://127.0.0.1",
        task_ignore_result=True,
)