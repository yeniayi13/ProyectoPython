# Usa una imagen base de Python
FROM python:3.12.3-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo de requisitos primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# Instala las dependencias sin almacenar cachés intermedios
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación escuche
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]