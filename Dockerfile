# Imagen base con Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Dependencias del servidor
RUN pip install --no-cache-dir fastapi uvicorn

# Código de la API
COPY Tienda_online/ .

# Puerto en el que escucha la API
EXPOSE 8000

# Arranque; 0.0.0.0 para aceptar conexiones desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
