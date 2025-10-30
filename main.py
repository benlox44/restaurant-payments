from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app= FastAPI()

class notificacion(BaseModel):
    catetoria: bool
    mensaje: str
    adicional: Optional[str]

#ruta base
@app.get("/")
def index():
    return {"message":"Hola mundo"}

#
@app.get("/mensajePago/{id}")
def mensajePago(id):
    return {"data": id}


@app.post("/notifications")
def notification(notificacion: notificacion):
    return {"message": f"notificacion {notificacion.mensaje} enviada"}