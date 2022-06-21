from os.path import abspath, join

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from ..orm import init

app = FastAPI(title="Wayback Archiver", description="A server for storing archival records by archiver clients.")

templates = Jinja2Templates(directory=abspath(join(__file__, "..", "..", "templates")))


@app.on_event("startup")
async def startup_event():
    await init()
