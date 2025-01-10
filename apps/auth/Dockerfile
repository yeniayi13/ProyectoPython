# Usa una imagen base de Python
FROM python:3.12.3-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias necesarias y Dockerize
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    mv dockerize /usr/local/bin/ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* dockerize-linux-amd64-v0.6.1.tar.gz

# Copia solo el archivo de requisitos primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# Instala las dependencias sin almacenar cachés intermedios
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación escuche
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["dockerize", "-wait", "tcp://rabbitmq:5672", "-timeout", "60s", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


