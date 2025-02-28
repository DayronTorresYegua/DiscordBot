import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Definir las variables de configuración
TOKEN = os.getenv("DISCORD_TOKEN")  # Token del bot
API_URL = os.getenv("API_URL")  # URL de la API
