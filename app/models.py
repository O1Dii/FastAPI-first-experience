from pydantic import BaseModel

# models have .dict() method. Just in case


class Item(BaseModel):
    name: str
    description: str = None
    price: float


class User(BaseModel):
    username: str
    full_name: str
