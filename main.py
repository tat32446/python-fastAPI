from fastapi import Body,FastAPI,Cookie,Header
from pydantic import BaseModel,Field
from typing import List,Set
from datetime import datetime, time, timedelta
from uuid import UUID

app=FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str = None

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: float = None
    is_offer:bool=None
    tags :Set[str]=[]
    images:List[Image]=None

class User(BaseModel):
    username: str
    full_name: str = None


class Offer(BaseModel):
    name: str
    description: str = None
    price: float
    items: List[Item]






@app.get('/')
def get_root():
    return {"Hello":"World"}

#If your code uses async / await, use async def:


@app.get('/items-one/{item_id}')
def read_item(item_id:int,query:str=None):
    return {"item_id":item_id,"query":query}

@app.put('/item/{item_id}')
def update_item(item_id:int,item:Item):
    return {"item_price":item.price,"item_id":item_id}


@app.get("/files/{file_path:path}")
async def read_user_me(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/fake_items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



@app.put("/items/{item_id}")
async def update_item(*, item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/advance/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(None),
    end_datetime: datetime = Body(None),
    repeat_at: time = Body(None),
    process_after: timedelta = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

@app.get("/cookie/")
async def read_items(*, ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}


@app.get("/header/")
async def read_items(*, user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/token/")
async def read_items(x_token: List[str] = Header(None)):
    return {"X-Token values": x_token}

@app.post("/user/", response_model=UserIn)
async def create_user(*, user: UserIn):
    return user