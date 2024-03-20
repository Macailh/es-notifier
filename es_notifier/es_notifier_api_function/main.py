from fastapi import FastAPI
from routers import notifier_router
from mangum import Mangum

app = FastAPI()

app.include_router(notifier_router.router, prefix="/api/v1")


handler = Mangum(app)
