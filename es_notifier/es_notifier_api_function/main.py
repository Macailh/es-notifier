import os
from fastapi import FastAPI
from routers import notifier_router
from mangum import Mangum

ROOT_PATH = os.getenv("ROOT_PATH", "")

app = FastAPI()
app.root_path = ROOT_PATH

app.include_router(notifier_router.router, prefix="/api/v1")


handler = Mangum(app)
