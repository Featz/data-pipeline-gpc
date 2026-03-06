import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# 1. Configuración de parámetros
LAT = 40.4168
LON = -3.7038
URL = "https://archive-api.open-meteo.com/v1/archive"

# 2. Fechas dinámicas (desde hace 3 años hasta ayer)
fecha_fin = datetime.now() - timedelta(days=1)
fecha_inicio = fecha_fin - timedelta(days=365*3)

fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')

parametros = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": fecha_inicio_str,
    "end_date": fecha_fin_str,
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "timezone": "auto"
}

print(f"Extrayendo datos desde {fecha_inicio_str} hasta {fecha_fin_str}...")

# 3. Petición a la API
respuesta = requests.get(URL, params=parametros)

if respuesta.status_code == 200:
    datos_crudos = respuesta.json()
    
    # 4. Transformación a DataFrame
    df = pd.DataFrame(datos_crudos["daily"])
    
    # 5. Añadir columnas de auditoría (Buenas prácticas)
    df['extraction_date'] = datetime.now()
    df['latitude'] = LAT
    df['longitude'] = LON
    
    # 6. Guardar en formato Parquet
    os.makedirs('data', exist_ok=True) # Crea la carpeta 'data' si no existe
    ruta_archivo = os.path.join('data', 'clima_historico.parquet')

    df.to_parquet(ruta_archivo, index=False)
    
    print(f"¡Éxito! {len(df)} filas guardadas en '{ruta_archivo}'.")
    
else:
    print(f"Error en la API. Código: {respuesta.status_code}")