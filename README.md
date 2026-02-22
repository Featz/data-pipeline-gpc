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

1. **Extract (`scripts/`)**: Un script desarrollado en **Python** consume datos meteorológicos desde una API pública gratuita.
2. **Load (`scripts/`)**: Los datos crudos (raw) son cargados de forma estructurada directamente a **Google BigQuery** (Data Warehouse).
3. **Transform (`dbt/`)**: Se utiliza **dbt** (Data Build Tool) conectado a BigQuery para limpiar, transformar y aplicar reglas de negocio sobre los datos crudos, modelando la información mediante tablas de dimensiones (ej. localidades) y hechos (ej. registros climáticos diarios).
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
├── dbt/                   # Contiene el proyecto de dbt, incluyendo perfiles de conexión, modelos (staging y marts), tests de dbt y macros.
├── scripts/               # Scripts de Python encargados del consumo de la API de Clima (Extract) y la inserción a GCP (Load).
├── tests/                 # Scripts con pruebas unitarias de los procesos en Python y la validación de la consistencia de los datos.
├── venv/                  # Entorno virtual de Python con las dependencias instaladas.
├── requirements.txt       # Listado de librerías de Python requeridas (Apache Airflow, dbt-bigquery, google-cloud-bigquery, pandas, etc.).
└── .gitignore             # Archivos y carpetas ignorados para el control de versiones en git.
```

## 🚀 Próximos pasos (Cómo usar este repositorio)

Para configurar e iniciar el desarrollo en local:

1. **Clonar este repositorio**

   ```bash
   git clone <url-del-repo>
   cd modern-data-pipeline-weather
   ```

2. **Crear e inicializar el entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar Credenciales (Google Cloud y API del Clima)**
   - Conseguir una API Key válida para el servicio de Weather elegido.
   - Configurar un `Service Account` en GCP para que el entorno tenga permisos de escritura y ejecución sobre BigQuery.

4. **Ejecutar dbt**
   - Asegurarse de tener configurado `profiles.yml` correctamente apuntando a BigQuery.

5. **Levantar localmente Apache Airflow**
   - Se puede inicializar la DB de Airflow mediante `airflow db init` y levantar el servidor web/scheduler local, o bien correr todo el empaquetado mediante una imagen de Docker.
