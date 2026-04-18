from sqlalchemy.orm import Session
from app.models.product import Product


def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session, name=None, category=None):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.contains(name))

    if category:
        query = query.filter(Product.category == category)

    return query.all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_stock(db: Session, product: Product, quantity: int):
    if product.quantity + quantity < 0:
        raise ValueError("Estoque não pode ser negativo")

    product.quantity += quantity
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()