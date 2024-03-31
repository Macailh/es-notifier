from fastapi import FastAPI
from routers import notifier_router
from mangum import Mangum
from config.env import ROOT_PATH


app = FastAPI()
app.root_path = ROOT_PATH

app.include_router(notifier_router.router, prefix="/api/v1")


handler = Mangum(app)
