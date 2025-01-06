from fastapi import FastAPI
from mangum import Mangum

from task_tracker.router import router

app = FastAPI(
    title="Task Tracker API",
    description="A simple API to manage personal tasks or to-do lists with FastAPI",
    version="1.0.0",
)

app.include_router(router)
handler = Mangum(app=app)
