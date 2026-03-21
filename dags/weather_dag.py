from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

ruta_proyecto = "/Users/frego/Documents/Proyects/modern-data-pipeline-weather"
ruta_extract = f"{ruta_proyecto}/scripts/extract.py"
ruta_dbt = f"{ruta_proyecto}/weather_transform"

# Configuración básica del DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1), # Fecha desde la que empieza a contar
    'retries': 1,                        # Si falla, reintenta 1 vez
    'retry_delay': timedelta(minutes=5), # Espera 5 min antes del reintento
}

# Definimos el DAG
with DAG(
    'weather_pipeline_dag',
    default_args=default_args,
    description='Orquestación de extracción API climática y transformación con dbt',
    schedule_interval='@daily',          # Queremos que corra una vez al día
    catchup=False                        # Evita que corra todo el historial de golpe
) as dag:

    # Tarea 1: Ejecutar el script de Python (Extracción)
    # Reemplaza la ruta por donde viva tu script y tu entorno virtual si usas uno
    extract_data = BashOperator(
        task_id='extract_weather_api',
        bash_command=f'python {ruta_extract}'
    )

    # Tarea 2: Ejecutar dbt run (Transformación Capa Staging y Oro)
    # Es vital usar 'cd' para que Airflow se posicione en la carpeta correcta antes de correr dbt
    dbt_run = BashOperator(
        task_id='dbt_run_models',
        bash_command=f'cd {ruta_dbt} && dbt run'
    )

    # Tarea 3: Ejecutar dbt test (Calidad de datos)
    dbt_test = BashOperator(
        task_id='dbt_test_data',
        bash_command=f'cd {ruta_dbt} && dbt test'
    )

    # Definir el orden de ejecución (Dependencias)
    # Esto le dice a Airflow: "No corras dbt hasta que la extracción termine con éxito"
    extract_data >> dbt_run >> dbt_test