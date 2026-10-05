import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="JARVIS Assistant", version="1.0")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

class Consulta(BaseModel):
    prompt: str
    usuario: str = "Luis"

@app.get("/")
def read_root():
    return {"mensaje": "¡JARVIS online con Groq!"}

@app.post("/chat")
def procesar_chat(datos: Consulta):
    # Lista de respaldo por si algún modelo llega a fallar
    modelos_disponibles = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-8b-8192"
    ]
    
    ultimo_error = None
    for modelo in modelos_disponibles:
        try:
            response = client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Eres JARVIS, un asistente virtual avanzado, inteligente, conciso y leal."},
                    {"role": "user", "content": datos.prompt}
                ]
            )
            return {
                "status": "success",
                "modelo_usado": modelo,
                "usuario": datos.usuario,
                "respuesta_jarvis": response.choices[0].message.content
            }
        except Exception as e:
            ultimo_error = str(e)
            continue
            
    raise HTTPException(status_code=500, detail=f"Error en todos los modelos: {ultimo_error}")
