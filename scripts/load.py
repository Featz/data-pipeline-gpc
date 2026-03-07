import os
import pandas as pd
from google.cloud import bigquery
import logging
from dotenv import load_dotenv

# 1. Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Obtener configuración (Twelve-Factor App)
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
DATASET_ID = os.getenv("GOOGLE_DATASET_ID")
TABLE_ID = "historical_weather" # Esto puede quedarse en el código al ser el nombre de la tabla final

# 3. Validación de seguridad (Programación defensiva)
if not PROJECT_ID or not DATASET_ID:
    raise ValueError("Faltan variables de entorno críticas. Verifica tu archivo .env")

# Nota: No necesitamos hacer os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ... 
# porque load_dotenv() ya lo ha inyectado en el sistema automáticamente.

def load_parquet_to_bigquery():
    """Lee el archivo Parquet local y lo sube a BigQuery."""
    # BigQuery tomará automáticamente el PROJECT_ID y las credenciales del entorno
    client = bigquery.Client(project=PROJECT_ID)
    
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    file_path = os.path.join('data', 'clima_historico.parquet')
    
    if not os.path.exists(file_path):
        logger.error(f"No se encontró el archivo: {file_path}. Ejecuta extract.py primero.")
        return

    logger.info(f"Leyendo datos locales desde {file_path}...")
    df = pd.read_parquet(file_path)
    
    logger.info(f"Subiendo {len(df)} filas a BigQuery ({table_ref})...")
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        logger.info("¡Carga completada exitosamente en BigQuery!")
    except Exception as e:
        logger.error(f"Error al subir a BigQuery: {e}")

if __name__ == "__main__":
    load_parquet_to_bigquery()