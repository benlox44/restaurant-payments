# Restaurant Payments API

Microservicio de pagos para restaurante usando Webpay Plus de Transbank.

**⚙️ Configurado para AMBIENTE DE INTEGRACIÓN (Testing)**

## 🚀 Características

- ✅ Crear transacciones de pago
- ✅ Confirmar transacciones después del pago
- ✅ Consultar estado de transacciones
- ✅ Realizar reembolsos
- ✅ Compatible con SDK Transbank versión 2.x y 3.x
- ✅ **Funciona en HTTP local (no requiere HTTPS para testing)**
- ✅ Credenciales de integración incluidas

## 📋 Requisitos Previos

- Python 3.8+
- pip
- (Opcional) Docker para containerización

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd restaurant-payments
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv fastapi-env
.\fastapi-env\Scripts\activate

# Linux/Mac
python3 -m venv fastapi-env
source fastapi-env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
# Desarrollo (con hot-reload)
uvicorn main:app --reload

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

**¡Listo!** El servidor estará en `http://localhost:8000`


**Credenciales de integración (ya incluidas):**
- Código de comercio: `597055555532`
- API Key: `579B532A7440BB0C9079DED94D31EA161EBE3BBA`

**Tarjeta de prueba:**
- Número: `4051 8856 0044 6623`
- CVV: `123`
- Fecha: `10/26`
- RUT: `11.111.111-1`
- Clave: `123`

## 🐳 Docker

### Desarrollo con Docker Compose

```bash
docker-compose up --build
```

## 🔐 Endpoints de la API

### 1. Crear Transacción

Inicia una nueva transacción de pago.

**Request:**
```http
POST /payments/create
Content-Type: application/json

{
  "buy_order": "orden-12345",
  "session_id": "session-abc123",
  "amount": 10000,
  "return_url": "https://tu-app.com/payment/return"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://webpay3gint.transbank.cl/webpayserver/...",
  "token": "01ab...",
  "buy_order": "orden-12345",
  "session_id": "session-abc123",
  "amount": 10000
}
```

### 2. Confirmar Transacción

Confirma una transacción después de que el usuario complete el pago.

**Request:**
```http
POST /payments/confirm
Content-Type: application/json

{
  "token": "01ab..."
}
```

**Response:**
```json
{
  "success": true,
  "vci": "TSY",
  "amount": 10000,
  "status": "AUTHORIZED",
  "buy_order": "orden-12345",
  "session_id": "session-abc123",
  "card_detail": {
    "card_number": "6623"
  },
  "accounting_date": "0320",
  "transaction_date": "2025-11-01T10:30:00.000Z",
  "authorization_code": "1213",
  "payment_type_code": "VD",
  "response_code": 0,
  "installments_amount": 0,
  "installments_number": 0,
  "balance": 0
}
```

### 3. Consultar Estado

Obtiene el estado actual de una transacción.

**Request:**
```http
GET /payments/status/{token}
```

**Response:**
```json
{
  "success": true,
  "status": "AUTHORIZED",
  "amount": 10000,
  "buy_order": "orden-12345",
  ...
}
```

### 4. Reembolsar

Realiza un reembolso total o parcial.

**Request:**
```http
POST /payments/refund
Content-Type: application/json

{
  "token": "01ab...",
  "amount": 10000
}
```

**Response:**
```json
{
  "success": true,
  "type": "REVERSED",
  "authorization_code": "1213",
  "authorization_date": "2025-11-01T10:35:00.000Z",
  "nullified_amount": 10000,
  "balance": 0,
  "response_code": 0
}
```

## 📊 Códigos de Respuesta

### Estados de Transacción
- `AUTHORIZED` - Transacción autorizada
- `FAILED` - Transacción fallida
- `REVERSED` - Transacción reversada

### Códigos VCI
- `TSY` - Autenticación exitosa
- `TSN` - Autenticación fallida
- `TO` - Timeout
- `ABO` - Abandonada por el usuario
- `U3` - Error interno

### Payment Type Codes
- `VD` - Venta Débito
- `VN` - Venta Normal
- `VC` - Venta en cuotas
- `SI` - 3 cuotas sin interés
- `S2` - 2 cuotas sin interés
- `NC` - N cuotas sin interés

## 🧪 Testing en Ambiente de Integración

### Credenciales de Integración (ya incluidas en el código)

```
Código de comercio: 597055555532
API Key: 579B532A7440BB0C9079DED94D31EA161EBE3BBA
Ambiente: Integración
```

## 📚 Documentación Interactiva

Una vez desplegado, visita:
- **Swagger UI**: `http://localhost:8000/docs`

## � Flujo de Pago

1. **Frontend** llama a `/payments/create` con datos de la orden
2. **Backend** crea transacción en Webpay y retorna `url` y `token`
3. **Frontend** redirige al usuario a la `url` de Webpay
    <form id="webpayForm" method="POST" action="https://webpay3gint.transbank.cl/webpayserver/initTransaction" style="display: none;">
        <input type="hidden" name="token_ws" id="token_ws">
    </form>
4. **Usuario** completa el pago en Webpay
5. **Webpay** redirige de vuelta a `return_url` con el `token`
6. **Frontend** llama a `/payments/confirm` con el `token`
7. **Backend** confirma la transacción y retorna el resultado

## 🛠️ Stack Tecnológico

- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Transbank SDK** - Integración oficial con Webpay Plus
- **Pydantic** - Validación de datos y serialización
- **Docker** - Containerización y deployment

## 📝 Notas Importantes

1. **Timeout**: Las transacciones en Webpay tienen un timeout de 10 minutos.
2. **Pruebas de pago**: se creo un html redirect_to_webpay.html para probar el acceso a la pasarela de pago