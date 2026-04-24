import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.product_routes import router as product_router
from .routes.auth_routes import router as auth_router

app = FastAPI(
    title="Stock FastAPI",
    description="API para gerenciamento de estoque de produtos",
    version="0.1.0"
)

# Configurar CORS PRIMEIRO (antes de outros middlewares)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir routers
app.include_router(product_router)
app.include_router(auth_router)


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "API is running"}


@app.get("/")
def root():
    return {"message": "Bem-vindo à Stock FastAPI"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
