from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola! Tu asistente JARVIS en Render está en línea y funcionando."}