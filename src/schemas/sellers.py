from pydantic import BaseModel
from .books import ReturnedBookInfo

class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class IncomingSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int 


class ReturnedSellerSilent(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSellerSilent]


class ReturnedSellerBooks(ReturnedSellerSilent):
    books: list[ReturnedBookInfo]


class UpdatedSeller(BaseModel):
    first_name: str
    last_name: str
    email: str