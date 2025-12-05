import os
from dotenv import load_dotenv, set_key
import secrets

load_dotenv()

def get_or_generate_jwt_secret():
    """Obtiene el secreto JWT de las variables de entorno o genera uno nuevo si no existe."""
    secret = os.getenv("SECRET_JWT")
    
    if not secret:
        print("SECRET_JWT not set. Generating new secret and saving to .env file...")
        secret = secrets.token_hex(32)
        
        # Save to .env file for persistence
        env_path = ".env"
        set_key(env_path, "SECRET_JWT", secret)
        
        # Set in current environment
        os.environ["SECRET_JWT"] = secret
    
    return secret
SECRET_JWT = get_or_generate_jwt_secret()

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "GeoControlDB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Configuración de debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"