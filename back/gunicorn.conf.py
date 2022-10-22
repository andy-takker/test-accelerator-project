from os import environ, cpu_count

bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1000
workers = int(environ.get("APP_WORKERS", cpu_count() // 2 + 1))
