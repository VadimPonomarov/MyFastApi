# Standard libraries
from typing import Any, Union

# Thirdparty libraries
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

import uvicorn

app = FastAPI()


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


with engine.connect() as conn:

    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
    conn.commit()

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET x=:x, y=:y WHERE y != :y"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
with Session(engine) as session:
    result = session.execute(stmt, {"y": 3})
    for row in result:
        print(f"xx: {row.x}  yy: {row.y}")
    session.commit()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World1"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
