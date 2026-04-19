from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..models.product import Product


def create_product(
    db: Session,
    data
    ):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(
    db: Session,
    name=None,
    category=None,
    skip=0,
    limit=10,
    order_by: str = "id",
    direction: str = "asc"
    ):
    query = db.query(Product).filter(Product.deleted == False)

    if name:
        query = query.filter(Product.name.contains(name))

    if category:
        query = query.filter(Product.category == category)

    column = getattr(Product, order_by, None)

    if column is not None:
        if direction == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    total = query.count()
    products = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "items": products
    }


def get_product(
    db: Session, 
    product_id: int
    ):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.deleted == False
        ).first()


def update_stock(
    db: Session,
    product: Product,
    quantity: int
    ):
    if product.quantity + quantity < 0:
        raise ValueError("Estoque não pode ser negativo")

    product.quantity += quantity
    db.commit()
    db.refresh(product)
    return product


def delete_product(
    db: Session,
    product: Product
    ):
    product.deleted = True
    db.commit()


def create_batch_products(
    db: Session,
    products_data: list
    ):
    """Cria múltiplos produtos em uma única transação"""
    products = []
    
    for data in products_data:
        product = Product(**data.dict())
        db.add(product)
        products.append(product)
    
    db.commit()
    
    # Refresh para obter os IDs gerados
    for product in products:
        db.refresh(product)
    
    return {
        "created": len(products),
        "items": products
    }