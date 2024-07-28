import os


wsgi_app = "app.api.main:app_factory()"

worker_class = "uvicorn.workers.UvicornWorker"

host = os.getenv("SERVER_HOST", "0.0.0.0")
port = os.getenv("SERVER_PORT", "8000")
bind = f"{host}:{port}"

workers = 4

daemon = False
