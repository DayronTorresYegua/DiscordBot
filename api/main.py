from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

@app.get("/personajes/{nombre}")
async def get_personaje(nombre: str):
    personaje = next((pj for pj in data["personajes"] if pj["nombre"].lower() == nombre), None)
    if personaje:
        personaje["imagen"] = f"/assets/{personaje['imagen']}"
        return personaje
    else:
        return {"error": "Personaje no encontrado"}
