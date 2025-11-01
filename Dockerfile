# Usa una imagen base de Python
FROM python:3.11-slim

# Variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto (Render usa variable $PORT)
EXPOSE 8000

# Comando para ejecutar la aplicación en producción
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}