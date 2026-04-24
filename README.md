# 📦 Stock FastAPI

A modern, scalable inventory management API built with **FastAPI**, **PostgreSQL**, and **Alembic migrations**.

---

## 🎯 Project Overview

Stock FastAPI is a RESTful backend service designed to manage product inventory with a clean, professional architecture. It provides endpoints to create, read, update, and delete products with batch operations support.

### ✨ Current Features

- **CRUD Operations**: Create, retrieve, update, and delete products
- **Batch Operations**: Insert multiple products in a single request
- **Product Management**: Track name, description, price, quantity, and category
- **JWT Authentication**: User registration and login with token-based security
- **User Management**: Create users, authenticate, and manage sessions
- **Database Versioning**: Alembic migrations for schema control
- **API Documentation**: Auto-generated Swagger UI at `/docs`
- **CORS Support**: Configured for cross-origin requests
- **Health Check**: Endpoint to verify API status
- **Docker Deployment**: Containerized with Docker Compose

---

## 🏗️ Project Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── database.py            # SQLAlchemy configuration & session management
├── models/
│   ├── product.py        # Product ORM model
│   └── user.py           # User ORM model for authentication
├── schemas/
│   ├── product_schemas.py # Pydantic validation schemas for products
│   └── user.py           # Pydantic schemas for user registration/login
├── routes/
│   ├── product_routes.py # API endpoints (v1/products)
│   └── auth_routes.py    # Authentication endpoints (v1/auth)
├── services/
│   ├── product_service.py # Business logic for products
│   ├── user_service.py   # User management logic
│   └── auth_service.py   # JWT token generation and validation
└── dependencies/
    └── auth.py           # Authentication dependencies

### Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.136+ |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0+ |
| Migrations | Alembic 1.18+ |
| Authentication | Python-Jose 3.5.0+ (JWT) |
| Password Hashing | Argon2-CFFI 25.1+ |
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

### Authentication

#### Register User
```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### Login
```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get All Users
```http
GET /v1/auth/users
```

#### Protected Route (Example)
```http
GET /v1/auth/protected
Authorization: Bearer <access_token>
```

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

### System

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "OK",
  "message": "API is running"
}
```

---

## 🗄️ Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| email | VARCHAR | User email (unique, indexed) |
| password | VARCHAR | Hashed password (Argon2) |

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

## � Quick Start: Authentication

After starting the API, authenticate with these steps:

1. **Register a new user**
   ```bash
   curl -X POST "http://localhost:8000/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
   ```

2. **Login to get a token**
   ```bash
   curl -X POST "http://localhost:8000/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
   ```

3. **Use the token in protected requests**
   ```bash
   curl -X GET "http://localhost:8000/v1/auth/protected" \
     -H "Authorization: Bearer <your_access_token>"
   ```

4. **Get all users**
   ```bash
   curl -X GET "http://localhost:8000/v1/auth/users"
   ```

---



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

## 🔐 Authentication Implementation

✅ **Completed Features:**

- User registration with email and password
- JWT token generation (60-minute expiration)
- Argon2 password hashing for security
- Authentication endpoints at `/v1/auth`
- Protected route example at `/v1/auth/protected`
- HTTPBearer security scheme integration

### How to Use Protected Endpoints

All endpoints can be protected with JWT authentication. Example:

```python
from typing import Annotated
from fastapi import Depends
from app.services.auth_service import get_current_user

@router.get("/protected")
def protected_endpoint(
    current_user: Annotated[str, Depends(get_current_user)]
):
    return {"user": current_user, "message": "This is protected"}
```

### Security Configuration

- **SECRET_KEY**: Set in `app/services/auth_service.py` (⚠️ Change in production)
- **ALGORITHM**: HS256
- **TOKEN_EXPIRY**: 60 minutes
- **Password Hash**: Argon2 (OWASP recommended)

---

## 🔐 Security Best Practices

✅ Implemented:
- Password hashing with Argon2
- JWT token validation
- CORS configuration
- SQLAlchemy ORM (SQL injection prevention)

📋 Recommended for Production:
- Use environment variables for `SECRET_KEY` and database credentials
- Enable HTTPS/TLS
- Implement rate limiting
- Add request logging and monitoring
- Use stronger CORS restrictions
- Enable CSRF protection if using cookies
- Implement password complexity requirements
- Add two-factor authentication (2FA)
- Use refresh tokens for better security

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

✅ CORS configuration for cross-origin requests

✅ Clean code structure (MVC pattern)

✅ HTTP status codes best practices

✅ Comprehensive error handling

✅ JWT authentication and authorization

✅ Argon2 password hashing (OWASP recommended)

✅ Health check endpoint for monitoring

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Status**: 🟢 Ready for production with JWT authentication implemented

**Last Updated**: April 2026

**Next Review**: After implementing one of the advanced features
