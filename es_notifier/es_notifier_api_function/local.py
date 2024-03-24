import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import notifier_router

load_dotenv(dotenv_path=".env.local", override=True)


app = FastAPI()
app.include_router(notifier_router.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("local:app", host="localhost", port=8000, reload=True)
