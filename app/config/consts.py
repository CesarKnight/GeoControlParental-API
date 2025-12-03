import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

# Configuración de debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"