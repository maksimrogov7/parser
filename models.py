from pydantic import BaseModel
class Item(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    supplier: str
    sale: int
    rating: float
    volume: int
    root: int
    feedbacks: int



class Items(BaseModel):
    products: list[Item]


