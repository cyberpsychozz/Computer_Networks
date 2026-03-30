from fastapi import FastAPI,  Query
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from db import init_db, save_to_db, get_all_repos
from parser import run_parser

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается, инициализирую БД...")
    init_db()
    yield
    print("Приложение завершает работу...")

app = FastAPI(lifespan=lifespan)

@app.get("/parse")
def parse(url: str = Query(..., description="URL для парсинга")):

    items = run_parser(url)
    save_to_db(items)

    return {"status": "success", "parsed_count": len(items), "url": url}

@app.get("/data")
def get_data():
    data = get_all_repos()
    return {"data": data}


