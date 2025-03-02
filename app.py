from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import uvicorn

app = FastAPI()

# Настройка статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Путь к JSON-файлу
JSON_PATH = Path("data/data.json")

@app.get("/")
async def show_json(request: Request):
    # Чтение JSON файла с проверкой существования
    if not JSON_PATH.exists():
        return {"error": "JSON file not found"}
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        json_data = json.dumps(json.load(f), indent=4, ensure_ascii=False)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "json_data": json_data
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)