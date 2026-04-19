import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.product_routes import router as product_router
from .database import create_all_tables

create_all_tables()

app = FastAPI(
    title="Stock FastAPI",
    description="API para gerenciamento de estoque de produtos",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(product_router)


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
