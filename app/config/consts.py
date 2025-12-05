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

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app/config/test.db")
SECRET_JWT = get_or_generate_jwt_secret()

# Configuración de debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"