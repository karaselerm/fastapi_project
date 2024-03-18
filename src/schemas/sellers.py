from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .books import ReturnedBookForSeller



class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str

class IncomingSeller(BaseSeller):
    password: str

class ReturnedSeller(BaseSeller):
    id: int

class ReturnedSeller_(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


class ReturnedSellerWithBooks(ReturnedSeller_):
    books: list[ReturnedBookForSeller]

    



