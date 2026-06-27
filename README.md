# NEXUS-DS

Plataforma MLOps contenerizada para predicción de churn en telecomunicaciones.
Proyecto de portafolio profesional basado en FastAPI, Streamlit y Floci (emulador AWS local).

## Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) >= 24.x (con Compose V2 incluido)
- [GNU Make](https://www.gnu.org/software/make/) (en Windows: instalar via [Chocolatey](https://chocolatey.org/) con `choco install make`)

## Primeros pasos

### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env si necesitas cambiar puertos (los valores por defecto funcionan en local)
```

### 2. Colocar el dataset

Descarga el dataset **Telco Customer Churn** (Kaggle) y coloca el archivo en:

```
data/raw/
```

El nombre y formato del archivo deben coincidir con el valor de `S3_DATASET_KEY` en tu `.env`
(por defecto: `raw/Telco_customer_churn.xlsx`). El sistema soporta `.xlsx`, `.xls` y `.csv`.

> El directorio `data/raw/` está en `.gitignore` — el dataset nunca se versiona.

### 3. Levantar la plataforma

```bash
make nexus-up
```

Esto construye las imágenes y levanta los 3 contenedores. La primera vez puede tardar unos minutos.

### 4. Inicializar recursos en la nube local

```bash
make nexus-init
```

Crea el bucket S3 en Floci y sube el dataset a S3.

---

## Comandos disponibles

| Comando          | Descripcion                                                  |
|------------------|--------------------------------------------------------------|
| `make nexus-up`    | Levanta los 3 contenedores (floci, nexus-api, nexus-ui)    |
| `make nexus-down`  | Detiene y elimina los contenedores                         |
| `make nexus-init`  | Inicializa bucket S3 y recursos en Floci                   |
| `make nexus-train` | Dispara el entrenamiento del modelo via API REST            |
| `make nexus-logs`  | Sigue los logs de todos los servicios en tiempo real       |
| `make nexus-test`  | Ejecuta el suite de tests dentro del contenedor de API     |
| `make nexus-status`| Verifica el estado de salud de los 3 servicios             |

---

## Arquitectura

| Servicio      | Descripcion                                                             |
|---------------|-------------------------------------------------------------------------|
| **floci**     | Emulador de AWS (S3, SSM) corriendo en `localhost:4566`                |
| **nexus-api** | API REST (FastAPI + uvicorn) expuesta en `localhost:8000`              |
| **nexus-ui**  | Dashboard interactivo (Streamlit) expuesto en `localhost:8501`         |

Los tres servicios corren en la red Docker interna `nexus-net`.
`nexus-api` y `nexus-ui` se comunican con `floci` usando el hostname de servicio (`floci:4566`), nunca `localhost`.
