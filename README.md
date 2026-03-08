# 🌤️ Modern Data Stack: Weather Data Pipeline

![Arquitectura ELT](https://img.shields.io/badge/Architecture-ELT-blue) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Airflow](https://img.shields.io/badge/Airflow-2.8-red) ![dbt](https://img.shields.io/badge/dbt-1.7-orange) ![BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue)

Este proyecto implementa flujo de datos robusto de principio a fin, aplicando el modelo **Modern Data Stack** (Core Data Engineering). Implementa un patrón **ELT (Extract, Load, Transform)** utilizando las mejores prácticas actuales del mercado para extraer información del clima de una API pública y llevarla hasta un entorno analítico en la nube.

## 🎯 Objetivo del Proyecto

El objetivo principal es demostrar la capacidad de extraer datos, cargarlos en un entorno Cloud (Google BigQuery) y transformarlos usando herramientas modernas como dbt, orquestando y automatizando todo el ciclo de vida del dato.

**Conceptos Aplicados:**

- Orquestación de procesos de datos.
- Flujo ELT (Extract, Load, Transform).
- Data Warehousing (Dimensiones y Hechos).

## 🏗️ Arquitectura del Proyecto

El pipeline de datos sigue los siguientes pasos estructurales:

1. **Extract (`scripts/extract.py`)**: Un script desarrollado en **Python** consume datos meteorológicos desde una API pública gratuita.
2. **Load (`scripts/load.py`)**: Los datos crudos (en formato Parquet) son cargados de forma estructurada directamente a **Google BigQuery** (Data Warehouse). El proceso utiliza `python-dotenv` para cargar variables de entorno seguras desde `.env` (sin exponer credenciales en el código), y la librería de BigQuery en Python para crear/sobrescribir tablas.
3. **Transform (`weather_transform/`)**: Se utiliza **dbt** (Data Build Tool) conectado a BigQuery para limpiar, transformar y aplicar reglas de negocio sobre los datos crudos. Hemos inicializado un proyecto dbt estructurado, configurado bajo `weather_transform/dbt_project.yml`.
   - **Staging (`models/staging/`)**: Contiene el modelo `stg_weather.sql` para limpieza y estandarización (casteo de tipos, renombramientos) sobre los datos crudos (`raw_data`).
   - **Tests y Documentación**: Definidos en `schema.yaml` para asegurar la calidad de datos (ej. tests de no nulos o duplicados en las fechas y validación de estructura de columnas).
4. **Orchestrate (`dags/`)**: Todo el flujo (Extracción, Carga y Transformación en dbt) está coordinado por **Apache Airflow**, programado para ejecutarse diariamente (Daily ETL).

## 🛠️ Stack Tecnológico

Las herramientas utilizadas son:

- **Python (requests, pandas, pyarrow):** Para ingesta, manipulación en memoria y preparación de formatos.
- **Google BigQuery:** Data Warehouse (Cloud).
- **dbt-bigquery:** Herramienta de transformación de datos mediante SQL modular.
- **Apache Airflow:** Orquestador (Data Pipeline Orchestration).

## 📂 Estructura del Repositorio

A continuación, se detalla la finalidad de cada carpeta dentro del proyecto:

```bash
modern-data-pipeline-weather/
├── dags/                  # Contiene los DAGs de Apache Airflow que orquestan las tareas (Extract, Load, Transform) diariamente.
├── data/                  # Directorio para almacenar data temporal localmente en formato CSV/Parquet antes de su carga final a BigQuery.
├── scripts/               # Scripts de Python encargados del consumo de la API (extract.py) y la carga a GCP (load.py) mediante variables .env.
├── weather_transform/     # Proyecto dbt inicializado con la estructura base, incluyendo dbt_project.yml para perfiles de conexión y modelos.
│   └── models/staging/    # Modelos de primera capa (stg_weather.sql) y definiciones de fuentes y tests (schema.yaml).
├── .env.example           # Plantilla de variables de entorno para usar dotenv, requeridas para GCP (Project ID, Dataset y Credenciales).
├── tests/                 # Scripts con pruebas unitarias de los procesos en Python y la validación de la consistencia de los datos.
├── venv/                  # Entorno virtual de Python con las dependencias instaladas.
├── requirements.txt       # Listado de librerías de Python requeridas (Apache Airflow, dbt-bigquery, google-cloud-bigquery, pandas, etc.).
└── .gitignore             # Archivos y carpetas ignorados para el control de versiones en git.
```

## 🚀 Próximos pasos (Cómo usar este repositorio)

Para configurar e iniciar el desarrollo en local:

1. **Clonar este repositorio**

   ```bash
   git clone https://github.com/Featz/data-pipeline-gpc
   cd data-pipeline-gpc
   ```

2. **Crear e inicializar el entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar Variables de Entorno y Credenciales**
   - Duplicar el archivo `.env.example` y renombrarlo a `.env`.
   - Modificar las variables de entorno en el `.env` (este archivo no se sube gracias al `.gitignore`):
     - `GOOGLE_PROJECT_ID`: El ID del proyecto en Google Cloud.
     - `GOOGLE_DATASET_ID`: El dataset creado en BigQuery (ej: `raw_data`).
     - `GOOGLE_APPLICATION_CREDENTIALS`: Ruta local al JSON de tu Service Account de GCP con permisos sobre BigQuery.

4. **Ejecutar Proceso de Carga (Load)**
   - Correr previamente la extracción (ej. `python scripts/extract.py`) para generar el archivo temporario parquet.
   - Ejecutar la carga mediante `python scripts/load.py`. Este módulo lee las variables y credenciales del archivo `.env` de forma transparente.

5. **Inicialización y Configuración de dbt**
   - El proyecto ya está inicializado dentro del directorio `weather_transform/` y configurado en base al archivo `dbt_project.yml`.
   - Dirígete a la carpeta respectiva: `cd weather_transform`
   - Configura el archivo `profiles.yml` (usualmente en `~/.dbt/profiles.yml`) para establecer la conexión a BigQuery.
   - Verifica el acceso con `dbt debug`.
   - Ejecuta las pruebas de calidad de datos con `dbt test` (verificará las reglas de `schema.yaml`).
   - Transforma los datos y construye los modelos ejecutando `dbt run`.

6. **Levantar localmente Apache Airflow**
   - Se puede inicializar la DB de Airflow mediante `airflow db init` y levantar el servidor web/scheduler local, o bien correr todo el empaquetado mediante una imagen de Docker.
