from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.get("/")
async def home():
    return {
        "Massage": "This is home page"
    }


@app.get('/task1')
async def read_task() -> list:
    return [
        {
            "Name": "Dior",
            "Password": "2004"
        },
        {
            "Name": "Toxir",
            "Password": "2005"
        }
    ]
