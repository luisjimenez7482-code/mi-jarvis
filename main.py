import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="JARVIS Assistant", version="1.0")

# Inicializar el cliente de OpenAI (tomará la clave de las variables de entorno)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Consulta(BaseModel):
    prompt: str
    usuario: str = "Luis"

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola! Tu asistente JARVIS con IA está en línea y funcionando."}

@app.get("/saludo/{nombre}")
def saludar_usuario(nombre: str):
    return {"mensaje": f"¡Saludos, {nombre}! Los sistemas de JARVIS están operativos y listos."}

@app.post("/chat")
def procesar_chat(datos: Consulta):
    try:
        # Llamada al modelo de inteligencia artificial
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres JARVIS, un asistente virtual avanzado, inteligente, conciso y leal."},
                {"role": "user", "content": datos.prompt}
            ]
        )
        
        # Extraer la respuesta del modelo
        respuesta_ia = response.choices[0].message.content
        
        return {
            "status": "success",
            "usuario": datos.usuario,
            "respuesta_jarvis": respuesta_ia
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
