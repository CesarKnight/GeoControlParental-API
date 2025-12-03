from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config.db import create_db_and_tables
from .routers import user_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicialización de recursos al iniciar la aplicación"""
    try:
        await create_db_and_tables()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise
    yield
    print("Application shutdown")

app = FastAPI(
    lifespan=lifespan,
    title="GeoControlParental API",
    description="API para control y gestión geolocalizada parental",
    version="1.0.0"
)

# Routers
app.include_router(user_route.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de GeoControlParental"}