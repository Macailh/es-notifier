from fastapi import FastAPI
from routers import notifier_router

app = FastAPI()

app.include_router(notifier_router.router, prefix="/api/v1")
