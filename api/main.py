from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Montar la carpeta de imágenes
app.mount("/assets", StaticFiles(directory="api/assets"), name="assets")

# Cargar datos de los personajes
with open("api/data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Endpoint para obtener informacion de un personaje
@app.get("/personajes/{nombre}")
async def get_personaje(nombre: str):
    personaje = next((pj for pj in data["personajes"] if pj["nombre"].lower() == nombre.lower()), None)
    
    if personaje:
        personaje["imagen"] = f"/assets/{personaje['imagen']}"
        return personaje
    else:
        return {"error": "Personaje no encontrado"}
