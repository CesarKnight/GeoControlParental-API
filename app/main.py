from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config.db import create_db_and_tables
# imports de fastapi-users
from .controllers.user_controller import auth_backend, current_active_user, fastapi_users
from .schemas.user_schemas import UserRead, UserCreate, UserUpdate
# Importar routers
from .routers import user_route
from .routers import auth_route


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
# User routers proveidos por fastapi-users
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix=auth_route.auth_router["prefix"], tags=auth_route.auth_router["tags"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix=auth_route.register_router["prefix"], tags=auth_route.register_router["tags"])
app.include_router(fastapi_users.get_reset_password_router(), prefix=auth_route.reset_password_router["prefix"], tags=auth_route.reset_password_router["tags"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix=auth_route.verify_router["prefix"], tags=auth_route.verify_router["tags"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix=user_route.users_router["prefix"], tags=user_route.users_router["tags"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de GeoControlParental"}