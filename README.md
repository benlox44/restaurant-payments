# Restaurant Payments API

Microservicio de pagos para restaurante usando Webpay Plus de Transbank.

## 🚀 Deployment en Render

### Opción 1: Con Docker (Recomendado)

1. Conecta tu repositorio de GitHub a Render
2. Crea un nuevo **Web Service**
3. Configura:
   - **Environment**: `Docker`
   - **Health Check Path**: `/health`
4. Agrega las variables de entorno:
   ```
   TRANSBANK_COMMERCE_CODE=597055555532
   TRANSBANK_API_KEY=tu_api_key_aqui
   ENVIRONMENT=production
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

## 🏗️ Desarrollo Local

### Con Docker:

```bash
# Construir y ejecutar
docker-compose up --build

# Detener
docker-compose down
```

### Sin Docker:

```bash
# Activar entorno virtual
.\fastapi-env\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Correr microservicio de pagos y notificaciones
uvicorn main:app --reload
```

## 📚 Documentación API

Una vez desplegado, visita:
- **Documentación Swagger**: `https://tu-app.onrender.com/docs`
- **ReDoc**: `https://tu-app.onrender.com/redoc`
- **Health Check**: `https://tu-app.onrender.com/health`

## 🔐 Endpoints

- `GET /` - Información de la API
- `GET /health` - Health check
- `POST /payments/create` - Crear transacción
- `POST /payments/confirm` - Confirmar pago
- `GET /payments/status/{token}` - Consultar estado
- `POST /payments/refund` - Reembolsar
- `POST /notifications` - Enviar notificación

## 🛠️ Stack Tecnológico

- **FastAPI** - Framework web
- **Uvicorn** - Servidor ASGI
- **Transbank SDK** - Integración Webpay Plus
- **Pydantic** - Validación de datos
- **Docker** - Containerización

## 🧪 Tarjeta de Prueba Transbank

Para testing en ambiente de integración:
- **Número**: 4051 8856 0044 6623
- **CVV**: 123
fecha: 10/26


# autentificacion
rut: 11.111.111-1
clave: 123


# api key secret: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C

# Webpay Plus: 597055555532

# Docker
docker-compose up -d