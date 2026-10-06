from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="JARVIS Assistant", version="1.0")

# Estructura para recibir datos por POST
class Consulta(BaseModel):
    prompt: str
    usuario: str = "Luis"

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola! Tu asistente JARVIS en Render está en línea y funcionando."}

# Nuevo endpoint GET con parámetro en la URL
@app.get("/saludo/{nombre}")
def saludar_usuario(nombre: str):
    return {"mensaje": f"¡Saludos, {nombre}! Los sistemas de JARVIS están operativos y a tu servicio."}

# Nuevo endpoint POST para procesar consultas
@app.post("/chat")
def procesar_chat(datos: Consulta):
    respuesta = f"Procesando instrucción de {datos.usuario}: '{datos.prompt}'. Todo en orden."
    return {
        "status": "success",
        "usuario": datos.usuario,
        "respuesta_jarvis": respuesta
    }
