from fastapi import Path, Query, Body, Cookie, Header, Form
# Path is used for path params like in '/smth/{item_id}' item_id
# Query used for query params
# Body is used to specify that param should be searched in request body

# Cookie for cookies
# Header for headers
# Form for form field

# By default path params are searched via kwargs
# basic types which were not found are query params
# pydantic models are body params

# We can use pydantic.Field as more global param definition

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app import app
from app.models import Item, User

items = {}


# For routes you can use APIRouter, check documentation
# DB connection may be any orm or anything, idk... SQLAlchemy as an example
# There are also BackgroundTasks classes in fastapi, see docs...
# You can customize and configure swagger with additional params, see docs...
# (Path Operation Configuration) for swagger

# Handling errors, files, static files, see docs...
# Middleware, see docs...
# Security, see docs...
# Dependencies, see docs...
# CORS, see docs...


@app.get('/', status_code=201)
async def index():
    return {'a': 1}


@app.get('/query/')
async def query(
        q: str = Query(..., min_length=5, regex='\s+[abc]+\s+'),  # ...-required
        q_default: str = None,
        q_list: list = Query(['a', 'b'])
):
    return {'q': q, 'q_default': q_default, 'q_list': q_list}


@app.get('/{item_id}/')
async def path(
        # gt ge lt le                                        for numeric ↓
        item_id: int = Path(..., title='the ID of item you want to get', gt=2),
        only_name: bool = False
):
    res = items.get(item_id)

    if not res:
        raise HTTPException(status_code=404, detail="Item not found")

    if only_name:
        return res.name

    return res


# response_model used for conversion, validation, limitation of output, etc.#
# different parameters of response can be specified there, see documentation
@app.post('/', response_model=Item)
async def post(item: Item, item_id: int):
    items[item_id] = item
    return item


@app.post('/post_models/')
async def post_models(
        item: Item,
        user: User,
        importance: int = Body(..., gt=0)
):
    return {'item': item, 'user': user, 'importance': importance}


@app.get('/cookie/')
async def cookie(cookies: str = Cookie(None)):
    return {'cookie': cookies}


@app.get('/headers/')
async def header(headers: str = Header(None)):  # it may be List[str]
    return {'headers': headers}


@app.post('/login/')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}
