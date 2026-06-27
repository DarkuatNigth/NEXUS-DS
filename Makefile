.PHONY: nexus-up nexus-down nexus-init nexus-train nexus-logs nexus-test nexus-status

# Levanta todos los contenedores (construye imágenes si es necesario)
nexus-up:
	docker compose up -d --build

# Detiene y elimina los contenedores
nexus-down:
	docker compose down

# Inicializa recursos en la nube local (bucket S3, SSM, etc.)
nexus-init:
	docker compose exec nexus-api python -m app.scripts.init_cloud

# Dispara el entrenamiento del modelo via API REST
nexus-train:
	curl -s -X POST http://localhost:8000/api/v1/train | python3 -m json.tool

# Sigue los logs de todos los servicios en tiempo real
nexus-logs:
	docker compose logs -f

# Ejecuta el suite de tests dentro del contenedor de API
nexus-test:
	docker compose exec nexus-api pytest /app/tests -v

# Verifica el estado de salud de los 3 servicios
nexus-status:
	@echo "=== NEXUS-DS Status ==="
	@curl -sf http://localhost:4566/_floci/health && echo "Floci: OK" || echo "Floci: DOWN"
	@curl -sf http://localhost:8000/health && echo "API: OK" || echo "API: DOWN"
	@curl -sf http://localhost:8501/_stcore/health && echo "UI: OK" || echo "UI: DOWN"
