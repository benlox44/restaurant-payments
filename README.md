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

**Ver guía completa de testing**: [`TESTING_LOCAL.md`](TESTING_LOCAL.md)

**Credenciales de integración (ya incluidas):**
- Código de comercio: `597055555532`
- API Key: `579B532A7440BB0C9079DED94D31EA161EBE3BBA`

**Tarjeta de prueba:**
- Número: `4051 8856 0044 6623`
- CVV: `123`
- Fecha: 10/26
- RUT: `11.111.111-1`
- Clave: `123`

## 🐳 Docker

### Desarrollo con Docker Compose

```bash
docker-compose up --build
```

### Producción

```bash
docker build -t restaurant-payments .
docker run -p 8000:8000 \
  -e WEBPAY_COMMERCE_CODE=tu_codigo \
  -e WEBPAY_API_KEY=tu_api_key \
  -e WEBPAY_ENV=production \
  restaurant-payments
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

### Tarjetas de Prueba

**Para transacciones exitosas:**
- Número: `4051 8856 0044 6623`
- CVV: `123`
- Fecha: Cualquier fecha futura (ej: `10/26`)

**Autenticación:**
- RUT: `11.111.111-1`
- Clave: `123`

### ⚠️ Importante

- ✅ **HTTP funciona para testing local** (no necesitas HTTPS)
- ✅ Puedes usar `http://localhost` en las URLs de retorno
- ✅ Las credenciales ya están en el código, no necesitas archivo .env
- ✅ Cada transacción debe tener `buy_order` y `session_id` únicos

## 🚀 Deployment en Render

### Opción 1: Con Docker (Recomendado)

1. Conecta tu repositorio de GitHub a Render
2. Crea un nuevo **Web Service**
3. Configura:
   - **Environment**: `Docker`
   - **Health Check Path**: `/health`
4. Agrega las variables de entorno:
   ```
   WEBPAY_COMMERCE_CODE=tu_codigo_comercio
   WEBPAY_API_KEY=tu_api_key
   WEBPAY_ENV=production
   ```

### Opción 2: Sin Docker

1. Conecta tu repositorio de GitHub a Render
2. Crea un nuevo **Web Service**
3. Configura:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`
   - **Health Check Path**: `/health`
4. Agrega las variables de entorno (igual que arriba)

## 📚 Documentación Interactiva

Una vez desplegado, visita:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🏗️ Arquitectura

```
restaurant-payments/
├── main.py                  # Aplicación FastAPI principal
├── Payment/
│   ├── webpay_service.py   # Lógica de Webpay Plus
│   └── __pycache__/
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación local
├── .env.example           # Template de variables de entorno
└── README.md              # Este archivo
```

## � Flujo de Pago

1. **Frontend** llama a `/payments/create` con datos de la orden
2. **Backend** crea transacción en Webpay y retorna `url` y `token`
3. **Frontend** redirige al usuario a la `url` de Webpay
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

1. **Seguridad**: Nunca expongas tu API Key en el código. Usa variables de entorno.
2. **Testing**: Siempre prueba en ambiente de integración antes de producción.
3. **Logs**: Monitorea los logs para detectar errores en transacciones.
4. **HTTPS**: En producción, usa siempre HTTPS para las URLs de retorno.
5. **Timeout**: Las transacciones en Webpay tienen un timeout de 10 minutos.

## 🐛 Troubleshooting

### Error: "Invalid commerce code"
- Verifica que `WEBPAY_COMMERCE_CODE` sea correcto
- Asegúrate de usar las credenciales correctas según el ambiente

### Error: "Invalid token"
- El token puede haber expirado (10 minutos)
- Verifica que estés usando el token correcto

### Error: "Transaction already committed"
- No puedes confirmar una transacción más de una vez
- Usa `/payments/status/{token}` para consultar el estado

## 📄 Licencia

Este proyecto está bajo la licencia MIT.