# 📦 Stock FastAPI

A modern, scalable inventory management API built with **FastAPI**, **PostgreSQL**, and **Alembic migrations**.

---

## 🎯 Project Overview

Stock FastAPI is a RESTful backend service designed to manage product inventory with a clean, professional architecture. It provides endpoints to create, read, update, and delete products with batch operations support.

### ✨ Current Features

- **CRUD Operations**: Create, retrieve, update, and delete products
- **Batch Operations**: Insert multiple products in a single request
- **Product Management**: Track name, description, price, quantity, and category
- **Database Versioning**: Alembic migrations for schema control
- **API Documentation**: Auto-generated Swagger UI at `/docs`
- **CORS Support**: Configured for cross-origin requests
- **Docker Deployment**: Containerized with Docker Compose

---

## 🏗️ Project Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── database.py            # SQLAlchemy configuration & session management
├── models/
│   └── product.py        # Product ORM model
├── schemas/
│   └── product_schemas.py # Pydantic validation schemas
├── routes/
│   └── product_routes.py # API endpoints (v1/products)
└── services/
    └── product_service.py # Business logic layer
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.136+ |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0+ |
| Migrations | Alembic |
| Package Manager | UV |
| Container | Docker & Docker Compose |
| Python | 3.14+ |

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.14+ (for local development)
- UV package manager

### Installation

1. **Clone & Setup**
   ```bash
   cd Stock_FASTAPI
   uv sync
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Apply Migrations**
   ```bash
   uv run alembic upgrade head
   ```

4. **Access API**
   - Swagger UI: http://localhost:8000/docs
   - API Base: http://localhost:8000

---

## 📋 API Endpoints

### Products

#### Create Product
```http
POST /v1/products
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 1500.00,
  "quantity": 5,
  "category": "Electronics"
}
```

#### List Products
```http
GET /v1/products?category=Electronics&skip=0&limit=10&order_by=price&direction=desc
```

#### Batch Create
```http
POST /v1/products/batch

{
  "products": [
    { "name": "Mouse", "price": 50.00, "quantity": 20, "category": "Peripherals" },
    { "name": "Keyboard", "price": 150.00, "quantity": 15, "category": "Peripherals" }
  ]
}
```

#### Update Stock
```http
PATCH /v1/products/{product_id}/stock?quantity=10
```

#### Delete Product
```http
DELETE /v1/products/{product_id}
```

---

## 🗄️ Database Schema

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR | Product name (indexed) |
| description | VARCHAR | Optional description |
| price | FLOAT | Product price |
| quantity | INTEGER | Stock quantity |
| category | VARCHAR | Product category (indexed) |
| deleted | BOOLEAN | Soft delete flag |

---

## 🔄 Database Migrations with Alembic

### Creating a Migration

Whenever you modify a model, create a migration:

```bash
uv run alembic revision --autogenerate -m "add field X to products"
```

### Applying Migrations

```bash
uv run alembic upgrade head
```

### Reverting Migrations

```bash
uv run alembic downgrade -1
```

### Viewing Migration History

```bash
uv run alembic history
```

---

## 🔐 Next Steps: Authentication with JWT

**Goal**: Secure all endpoints with JWT authentication

### Implementation Plan

1. **Install Dependencies**
   ```bash
   uv add python-jose[cryptography] pydantic-settings
   ```

2. **Create User Model**
   - Add `User` table with email, hashed password
   - Create migration: `uv run alembic revision --autogenerate -m "create users table"`

3. **Implement Authentication Service**
   - Password hashing (bcrypt)
   - JWT token generation and validation
   - Login endpoint: `POST /auth/login`

4. **Secure Endpoints**
   - Create `Depends()` for JWT verification
   - Protect product endpoints with `@require_auth`
   - Add user context to operations (audit trail)

5. **Testing**
   - Test login flow
   - Verify token-protected endpoints
   - Test token refresh mechanism

### Example Protected Endpoint

```python
@router.post("/v1/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    return product_service.create_product(db, product, created_by=current_user.id)
```

---

## 🎯 Alternative Roadmap Options

After JWT implementation, choose your next feature:

### 2️⃣ Advanced Inventory Features
- Low stock alerts
- Inventory history/audit logs
- Supplier management
- Barcode/SKU support

### 3️⃣ Analytics & Reporting
- Sales dashboard
- Stock trends
- Category performance
- Revenue reports

### 4️⃣ Integration Layer
- Webhook support for external systems
- API rate limiting
- Request logging & monitoring
- Third-party vendor APIs

---

## 🧪 Testing & Validation

### Run Type Checking
```bash
uv run mypy app/
```

### Lint Code
```bash
uv run flake8 app/
```

### Format Code
```bash
uv run black app/
```

---

## 📊 Development Workflow

1. **Feature Branch**
   ```bash
   git checkout -b feature/jwt-auth
   ```

2. **Make Changes** (update models, create migration)
   ```bash
   uv run alembic revision --autogenerate -m "describe change"
   ```

3. **Test Locally**
   ```bash
   uv run alembic upgrade head
   docker-compose restart api
   ```

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: add JWT authentication"
   git push origin feature/jwt-auth
   ```

---

## 🐳 Docker Compose Details

### Services

**estoque_db** (PostgreSQL)
- Image: postgres:16
- Port: 5432
- Database: estoque_db
- Credentials: postgres/postgres

**estoque_api** (FastAPI)
- Port: 8000
- Environment: DATABASE_URL from compose
- Depends on: estoque_db (healthy)

### Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f estoque_api

# Rebuild image
docker-compose up -d --build
```

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Pydantic Validation](https://docs.pydantic.dev/)

---

## 💡 Best Practices Implemented

✅ Dependency injection with `Depends()`
✅ Annotated type hints for clarity
✅ Service layer for business logic separation
✅ Schema validation with Pydantic
✅ Database migrations for versioning
✅ Soft delete support (deleted flag)
✅ CORS configuration
✅ Clean code structure (MVC pattern)
✅ HTTP status codes best practices
✅ Comprehensive error handling

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Status**: 🟢 Ready for authentication implementation

**Next Review**: After JWT implementation
