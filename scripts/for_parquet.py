import pyarrow.parquet as pq

# Lee solo la metadata (instantáneo y no consume memoria)
archivo = pq.ParquetFile('data/clima_historico.parquet')

print(f"Filas totales: {archivo.metadata.num_rows}")
print(f"Columnas: {archivo.metadata.num_columns}")
print("\n--- ESQUEMA (Tipos de datos) ---")
print(archivo.schema)