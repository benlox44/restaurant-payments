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

# Endpoint de retorno desde Webpay (ejemplo)
@app.get("/payment/callback")
def payment_callback(token_ws: str = None):
    """
    Endpoint de ejemplo para recibir el retorno de Webpay
    
    Webpay redirigirá aquí después del pago con el parámetro token_ws
    URL de retorno ejemplo: http://localhost:8000/payment/callback
    
    Este endpoint:
    1. Recibe el token_ws de Webpay
    2. Confirma automáticamente la transacción
    3. Muestra el resultado en HTML
    """
    from fastapi.responses import HTMLResponse
    
    if not token_ws:
        return HTMLResponse("""
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: red;">❌ Error</h1>
                    <p>No se recibió el token de Webpay</p>
                    <a href="/">Volver al inicio</a>
                </body>
            </html>
        """)
    
    try:
        # Confirmar la transacción automáticamente
        resultado = webpay_service.commit_transaction(token=token_ws)
        
        if not resultado.get("success"):
            return HTMLResponse(f"""
                <html>
                    <body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h1 style="color: red;">❌ Error al confirmar</h1>
                        <p>{resultado.get('error')}</p>
                        <a href="/">Volver al inicio</a>
                    </body>
                </html>
            """)
        
        status = resultado.get("status")
        amount = resultado.get("amount")
        auth_code = resultado.get("authorization_code")
        buy_order = resultado.get("buy_order")
        response_code = resultado.get("response_code")
        
        if status == "AUTHORIZED" and response_code == 0:
            # Pago exitoso
            return HTMLResponse(f"""
                <html>
                    <head>
                        <title>Pago Exitoso</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                text-align: center;
                                padding: 50px;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                            }}
                            .card {{
                                background: white;
                                color: #333;
                                padding: 40px;
                                border-radius: 15px;
                                max-width: 500px;
                                margin: 0 auto;
                                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                            }}
                            .success {{
                                color: #28a745;
                                font-size: 60px;
                                margin: 0;
                            }}
                            .info {{
                                margin: 20px 0;
                                padding: 15px;
                                background: #f8f9fa;
                                border-radius: 8px;
                            }}
                            .label {{
                                font-weight: bold;
                                color: #666;
                            }}
                            .value {{
                                color: #333;
                                font-size: 18px;
                            }}
                            a {{
                                display: inline-block;
                                margin-top: 20px;
                                padding: 12px 30px;
                                background: #667eea;
                                color: white;
                                text-decoration: none;
                                border-radius: 5px;
                                transition: background 0.3s;
                            }}
                            a:hover {{
                                background: #764ba2;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="card">
                            <div class="success">✅</div>
                            <h1>¡Pago Exitoso!</h1>
                            <p>Tu transacción ha sido procesada correctamente</p>
                            
                            <div class="info">
                                <div class="label">Monto</div>
                                <div class="value">${amount:,} CLP</div>
                            </div>
                            
                            <div class="info">
                                <div class="label">Orden de Compra</div>
                                <div class="value">{buy_order}</div>
                            </div>
                            
                            <div class="info">
                                <div class="label">Código de Autorización</div>
                                <div class="value">{auth_code}</div>
                            </div>
                            
                            <div class="info">
                                <div class="label">Token</div>
                                <div class="value" style="font-size: 12px; word-break: break-all;">{token_ws[:20]}...</div>
                            </div>
                            
                            <a href="/">Volver al inicio</a>
                        </div>
                    </body>
                </html>
            """)
        else:
            # Pago rechazado
            return HTMLResponse(f"""
                <html>
                    <head>
                        <title>Pago Rechazado</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                text-align: center;
                                padding: 50px;
                                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                color: white;
                            }}
                            .card {{
                                background: white;
                                color: #333;
                                padding: 40px;
                                border-radius: 15px;
                                max-width: 500px;
                                margin: 0 auto;
                                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                            }}
                            .error {{
                                color: #dc3545;
                                font-size: 60px;
                                margin: 0;
                            }}
                            a {{
                                display: inline-block;
                                margin-top: 20px;
                                padding: 12px 30px;
                                background: #dc3545;
                                color: white;
                                text-decoration: none;
                                border-radius: 5px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="card">
                            <div class="error">❌</div>
                            <h1>Pago Rechazado</h1>
                            <p>La transacción no pudo ser procesada</p>
                            <p><strong>Estado:</strong> {status}</p>
                            <p><strong>Código de respuesta:</strong> {response_code}</p>
                            <a href="/">Intentar nuevamente</a>
                        </div>
                    </body>
                </html>
            """)
            
    except Exception as e:
        return HTMLResponse(f"""
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: red;">❌ Error</h1>
                    <p>Error al procesar el pago: {str(e)}</p>
                    <a href="/">Volver al inicio</a>
                </body>
            </html>
        """)

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)