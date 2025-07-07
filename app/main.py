from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
import os
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

if not STATIC_DIR.exists():
    raise Exception(f"Directory {STATIC_DIR} does not exist")
if not TEMPLATES_DIR.exists():
    raise Exception(f"Directory {TEMPLATES_DIR} does not exist")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

GAME_FILE_PATH = STATIC_DIR / "downloads" / "game_setup.exe"
GAME_FILE_NAME = "awesome_game_setup.exe"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download")
async def download_game():
    if GAME_FILE_PATH.exists():
        return FileResponse(
            GAME_FILE_PATH,
            filename=GAME_FILE_NAME,
            media_type='application/octet-stream'
        )
    return {"error": "File not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)