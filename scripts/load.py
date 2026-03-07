import os
import pandas as pd
from google.cloud import bigquery
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 1. Autenticación: Le decimos a Python dónde está la llave JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data-weather-demo-78de1f5e8858.json"

# 2. Configuración de destino (¡CAMBIA EL PROJECT_ID!)
PROJECT_ID = "933465459702"  
DATASET_ID = "raw_data"
TABLE_ID = "historical_weather"

def load_parquet_to_bigquery():
    """Lee el archivo Parquet local y lo sube a BigQuery."""
    client = bigquery.Client()
    
    # Ruta de la tabla en la nube: proyecto.dataset.tabla
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    file_path = os.path.join('data', 'clima_historico.parquet')
    
    if not os.path.exists(file_path):
        logger.error(f"No se encontró el archivo: {file_path}. Ejecuta extract.py primero.")
        return

    logger.info(f"Leyendo datos locales desde {file_path}...")
    df = pd.read_parquet(file_path)
    
    logger.info(f"Subiendo {len(df)} filas a BigQuery ({table_ref})...")
    
    # Configuración: WRITE_TRUNCATE reemplaza la tabla si ya existe
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Esperamos a que Google termine
        logger.info("¡Carga completada exitosamente en BigQuery!")
    except Exception as e:
        logger.error(f"Error al subir a BigQuery: {e}")

if __name__ == "__main__":
    load_parquet_to_bigquery()