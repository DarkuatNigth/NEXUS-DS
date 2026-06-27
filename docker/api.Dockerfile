FROM python:3.10-slim

WORKDIR /app

# Copia solo el archivo de dependencias para aprovechar la caché de Docker.
# El código fuente NO se copia aquí — se monta via bind mount en docker-compose.yml.
COPY services/api/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--reload-dir", "/app/app", "--host", "0.0.0.0", "--port", "8000"]
