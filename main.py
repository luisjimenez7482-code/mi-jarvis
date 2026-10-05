import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="JARVIS Assistant", version="1.0")

# Inicializar el cliente apuntando a Groq y usando su variable de entorno
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

class Consulta(BaseModel):
    prompt: str
    usuario: str = "Luis"

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola! Tu asistente JARVIS con IA gratuita está en línea."}

@app.get("/saludo/{nombre}")
def saludar_usuario(nombre: str):
    return {"mensaje": f"¡Saludos, {nombre}! Los sistemas de JARVIS están operativos."}

@app.post("/chat")
def procesar_chat(datos: Consulta):
    try:
        # Llamada usando un modelo gratuito y rapidísimo de Groq
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Eres JARVIS, un asistente virtual avanzado, inteligente, conciso y leal."},
                {"role": "user", "content": datos.prompt}
            ]
        )
        
        respuesta_ia = response.choices[0].message.content
        
        return {
            "status": "success",
            "usuario": datos.usuario,
            "respuesta_jarvis": respuesta_ia
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
