# 🧪 Guía de Testing Local - Webpay Plus

## ✅ Se Puede Probar en Local (HTTP)

**¡SÍ! No necesitas HTTPS para testing.** El ambiente de integración de Transbank funciona perfectamente con `http://localhost`.

## 🚀 Configuración Actual

Este microservicio está configurado **SOLO PARA INTEGRACIÓN** con credenciales hardcodeadas:

- **Código de comercio**: `597055555532`
- **API Key**: `579B532A7440BB0C9079DED94D31EA161EBE3BBA`
- **Ambiente**: Integración (Testing)

## 📝 Pasos para Probar en Local

### 1. Iniciar tu servidor de pagos (Backend)

```powershell
# Activar entorno virtual
.\fastapi-env\Scripts\activate

# Ejecutar servidor
uvicorn main:app --reload
```

El servidor estará en: `http://localhost:8000`

### 2. Crear una transacción

Puedes usar cualquiera de estos métodos:

#### Opción A: Swagger UI (Más fácil) 🌟

1. Abre en tu navegador: http://localhost:8000/docs
2. Busca `POST /payments/create`
3. Click en "Try it out"
4. Usa este JSON:

```json
{
  "buy_order": "orden-test-123",
  "session_id": "session-test-123",
  "amount": 15000,
  "return_url": "http://localhost:8000/"
}
```

5. Click "Execute"
6. Copia el `token` y la `url` de la respuesta

#### Opción B: PowerShell

```powershell
$body = @{
    buy_order = "orden-test-$(Get-Random)"
    session_id = "session-test-$(Get-Random)"
    amount = 15000
    return_url = "http://localhost:8000/"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/payments/create" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Ver respuesta
$response

# Guardar token y URL
$token = $response.token
$url = $response.url

Write-Host "Token: $token"
Write-Host "URL de Webpay: $url"
```

#### Opción C: Frontend de Ejemplo

Abre el archivo `frontend_example.html` en tu navegador y sigue los pasos.

### 3. Ir a Webpay para completar el pago

1. Toma la `url` que recibiste en la respuesta
2. Ábrela en tu navegador
3. Verás el formulario de pago de Webpay (ambiente de integración)

**Usa estos datos de prueba:**

- **Tarjeta**: `4051 8856 0044 6623`
- **CVV**: `123`
- **Fecha de vencimiento**: Cualquier fecha futura (ej: `10/26`)

Click en "Continuar"

- **RUT**: `11.111.111-1`
- **Clave**: `123`

Click en "Aceptar"

### 4. Confirmar la transacción

Después de completar el pago, Webpay te redirigirá de vuelta con un `token_ws` en la URL.

**Confirmar usando Swagger:**

1. Ve a http://localhost:8000/docs
2. Busca `POST /payments/confirm`
3. Click "Try it out"
4. Ingresa tu token:

```json
{
  "token": "tu-token-aqui"
}
```

5. Click "Execute"

**Confirmar usando PowerShell:**

```powershell
$confirmBody = @{
    token = $token  # O reemplaza con tu token
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/payments/confirm" `
    -Method POST `
    -Body $confirmBody `
    -ContentType "application/json"

# Ver resultado
$result

# Verificar si fue exitoso
if ($result.status -eq "AUTHORIZED" -and $result.response_code -eq 0) {
    Write-Host "✅ PAGO EXITOSO!" -ForegroundColor Green
    Write-Host "Código de autorización: $($result.authorization_code)"
    Write-Host "Monto: $($result.amount)"
} else {
    Write-Host "❌ Pago rechazado" -ForegroundColor Red
}
```

## 🎯 Flujo Completo de Testing

```
1. POST /payments/create
   ↓ (recibes url y token)
   
2. Abrir url en navegador
   ↓ (completar pago en Webpay)
   
3. Webpay redirige a return_url
   ↓ (con token_ws en la URL)
   
4. POST /payments/confirm (con el token)
   ↓ (recibes confirmación)
   
5. ✅ Pago completado
```

## 📊 Verificar Estado de una Transacción

```powershell
# Reemplaza TOKEN_AQUI con tu token real
Invoke-RestMethod -Uri "http://localhost:8000/payments/status/TOKEN_AQUI"
```

O en Swagger: `GET /payments/status/{token}`

## 💡 URLs Válidas para return_url en Testing Local

Todas estas funcionan perfectamente:

```
✅ http://localhost:8000/
✅ http://localhost:3000/payment/return
✅ http://localhost:5173/checkout/success
✅ http://127.0.0.1:8000/payment/callback
```

## ⚠️ Notas Importantes

1. **No necesitas HTTPS para testing local** ✅
2. El ambiente de integración acepta URLs `http://localhost` sin problema
3. Las credenciales están hardcodeadas, no necesitas archivo `.env`
4. Cada transacción es única, usa diferentes `buy_order` y `session_id`
5. Los tokens expiran en 10 minutos
6. No puedes confirmar la misma transacción dos veces

## 🐛 Solución de Problemas

### Error: "Invalid token"
- El token expiró (10 minutos)
- Estás usando un token incorrecto
- Ya confirmaste esa transacción

### Error: "Connection refused"
- Asegúrate de que el servidor esté corriendo en http://localhost:8000
- Verifica con: `curl http://localhost:8000/health`

### No redirige después del pago
- Revisa que tu `return_url` sea válida
- Webpay agregará el `token_ws` como parámetro

## 🎉 Testing Exitoso

Si ves esto en la respuesta de `/payments/confirm`:

```json
{
  "success": true,
  "status": "AUTHORIZED",
  "response_code": 0,
  "authorization_code": "1213",
  "amount": 15000
}
```

**¡Felicitaciones! El pago fue exitoso** ✅

## 📱 Ejemplo Completo con Frontend

Si tienes un frontend (React, Vue, etc.) corriendo en `http://localhost:3000`:

```javascript
// 1. Crear transacción
const response = await fetch('http://localhost:8000/payments/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    buy_order: 'orden-' + Date.now(),
    session_id: 'session-' + Date.now(),
    amount: 15000,
    return_url: 'http://localhost:3000/payment/return'
  })
});

const data = await response.json();

// 2. Redirigir a Webpay
window.location.href = data.url + '?token_ws=' + data.token;

// 3. En tu página de retorno (http://localhost:3000/payment/return)
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token_ws');

// 4. Confirmar transacción
const confirmResponse = await fetch('http://localhost:8000/payments/confirm', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token })
});

const result = await confirmResponse.json();

if (result.status === 'AUTHORIZED') {
  console.log('✅ Pago exitoso!');
}
```

## 🔒 Cuando Pases a Producción

**Entonces SÍ necesitarás:**
- ✅ HTTPS obligatorio
- ✅ Credenciales reales de Transbank
- ✅ Modificar el código para usar `build_for_production()`
- ✅ URLs de retorno con HTTPS

Pero para desarrollo y testing, **HTTP local funciona perfecto** 👍
