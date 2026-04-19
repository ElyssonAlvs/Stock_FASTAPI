from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int
    category: str


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]


class BatchProductCreate(BaseModel):
    products: list[ProductCreate]


class BatchProductResponse(BaseModel):
    created: int
    items: list[ProductResponse]
