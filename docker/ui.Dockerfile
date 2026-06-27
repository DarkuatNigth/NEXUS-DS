FROM python:3.10-slim

WORKDIR /app

# Copia solo el archivo de dependencias para aprovechar la caché de Docker.
# El código fuente NO se copia aquí — se monta via bind mount en docker-compose.yml.
COPY services/ui/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.runOnSave", "true", "--server.address", "0.0.0.0", "--server.port", "8501"]
