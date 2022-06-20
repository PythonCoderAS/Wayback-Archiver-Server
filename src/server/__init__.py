from fastapi import FastAPI

from ..orm import init

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init()
