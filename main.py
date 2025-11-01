from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from Payment.webpay_service import webpay_service
import os

app = FastAPI(
    title="Restaurant Payments API",
    description="Microservicio de pagos para restaurante usando Webpay Plus",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Notificacion(BaseModel):
    categoria: bool = Field(..., description="Categoría de la notificación")
    mensaje: str = Field(..., description="Mensaje de la notificación")
    adicional: Optional[str] = Field(None, description="Información adicional")

class TransaccionCrear(BaseModel):
    buy_order: str = Field(..., max_length=26, description="Orden de compra")
    session_id: str = Field(..., description="ID de sesión")
    amount: float = Field(..., gt=0, description="Monto de la transacción")
    return_url: str = Field(..., description="URL de retorno")

class TransaccionConfirmar(BaseModel):
    token: str = Field(..., description="Token de la transacción")

class Reembolso(BaseModel):
    token: str = Field(..., description="Token de la transacción")
    amount: float = Field(..., gt=0, description="Monto a reembolsar")

# Ruta base
@app.get("/")
def index():
    return {
        "message": "API de Pagos del Restaurante",
        "version": "1.0.0",
        "status": "active"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Crear transacción de pago
@app.post("/payments/create")
def crear_pago(transaccion: TransaccionCrear):
    """Crea una nueva transacción de pago con Webpay Plus"""
    try:
        resultado = webpay_service.create_transaction(
            buy_order=transaccion.buy_order,
            session_id=transaccion.session_id,
            amount=transaccion.amount,
            return_url=transaccion.return_url
        )
        
        if not resultado.get("success"):
            raise HTTPException(status_code=400, detail=resultado.get("error"))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Confirmar transacción
@app.post("/payments/confirm")
def confirmar_pago(confirmacion: TransaccionConfirmar):
    """Confirma una transacción después del pago"""
    try:
        resultado = webpay_service.commit_transaction(token=confirmacion.token)
        
        if not resultado.get("success"):
            raise HTTPException(status_code=400, detail=resultado.get("error"))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener estado de pago
@app.get("/payments/status/{token}")
def estado_pago(token: str):
    """Obtiene el estado de una transacción"""
    try:
        resultado = webpay_service.get_status(token=token)
        
        if not resultado.get("success"):
            raise HTTPException(status_code=400, detail=resultado.get("error"))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reembolsar pago
@app.post("/payments/refund")
def reembolsar_pago(reembolso: Reembolso):
    """Realiza un reembolso de una transacción"""
    try:
        resultado = webpay_service.refund_transaction(
            token=reembolso.token,
            amount=reembolso.amount
        )
        
        if not resultado.get("success"):
            raise HTTPException(status_code=400, detail=resultado.get("error"))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint legacy - mantener para compatibilidad
@app.get("/mensajePago/{id}")
def mensaje_pago(id: str):
    """Endpoint legacy para mensajes de pago"""
    return {"data": id, "message": "Use /payments/status/{token} instead"}

# Enviar notificaciones
@app.post("/notifications")
def notification(notificacion: Notificacion):
    """Envía una notificación"""
    return {
        "success": True,
        "message": f"Notificación '{notificacion.mensaje}' enviada",
        "categoria": notificacion.categoria,
        "adicional": notificacion.adicional
    }

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)