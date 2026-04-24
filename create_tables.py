#!/usr/bin/env python3
from app.database import Base, engine
from app.models.user import User
from app.models.product import Product

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
