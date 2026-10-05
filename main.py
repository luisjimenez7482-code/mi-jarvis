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
    # Usamos únicamente el modelo actual y estable
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres JARVIS, un asistente virtual avanzado, inteligente, conciso y leal."},
                {"role": "user", "content": datos.prompt}
            ]
        )
        return {
            "status": "success",
            "usuario": datos.usuario,
            "respuesta_jarvis": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
