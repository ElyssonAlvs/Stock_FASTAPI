from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.product_schemas import (
    ProductCreate,
    ProductResponse,
    ProductListResponse,
    BatchProductCreate,
    BatchProductResponse
)
from ..services import product_service

router = APIRouter(prefix="/v1/products", tags=["Products"])


@router.post("", response_model=ProductResponse)
def create(
    product: ProductCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return product_service.create_product(db, product)


@router.post("/batch", response_model=BatchProductResponse)
def create_batch(
    batch: BatchProductCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return product_service.create_batch_products(db, batch.products)


@router.get("", response_model=ProductListResponse)
def list_products(
    db: Annotated[Session, Depends(get_db)],
    name: Annotated[str | None, Query()] = None,
    category: Annotated[str | None, Query()] = None,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
    order_by: str = "id",
    direction: str = "asc"
):
    return product_service.get_products(db, name, category, skip, limit, order_by, direction)


@router.patch("/{product_id}/stock")
def update_stock(
    product_id: Annotated[int, Path()],
    quantity: Annotated[int, Query()],
    db: Annotated[Session, Depends(get_db)]
):
    product = product_service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")

    try:
        return product_service.update_stock(db, product, quantity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}")
def delete(
    product_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)]
):
    product = product_service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")

    product_service.delete_product(db, product)
    return {"ok": True}
