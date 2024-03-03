from pydantic import BaseModel, Field

from .books import ReturnedBookInfo

__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedSellerBooks", "ReturnedAllSellers", "UpdatedSeller"]


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class IncomingSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int

class ReturnedSellerBooks(BaseSeller):
    books: list[ReturnedBookInfo]

class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]

class UpdatedSeller(BaseModel):
    first_name: str
    last_name: str
    email: str    