from fastapi import FastAPI

from ..orm import init

app = FastAPI(title="Wayback Archiver", description="A server for storing archival records by archiver clients.")


@app.on_event("startup")
async def startup_event():
    await init()
