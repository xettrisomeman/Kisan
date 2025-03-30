from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_database

import rest_goods
import rest_users
import rest_buy


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables (if not exist)...")
    create_database()
    yield
    print("Application is shutting down...")


app = FastAPI(lifespan=lifespan)


app.include_router(rest_goods.router)
app.include_router(rest_users.router)
app.include_router(rest_buy.router)


@app.get("/")
def main():
    return {"message": "home"}
