WITH raw_data AS (
    -- Aquí llamamos a la fuente tal cual la definimos en el schema.yml
    SELECT * FROM {{ source('weather_source', 'historical_data') }}
)

SELECT
    -- Renombramos y aseguramos los tipos de datos correctos
    CAST(time AS DATE) AS observation_date,
    
    CAST(temperature_2m_max AS FLOAT64) AS max_temperature_c,
    CAST(temperature_2m_min AS FLOAT64) AS min_temperature_c,
    
    -- Corregimos el nombre de la columna de precipitación
    CAST(preciptacion_sum AS FLOAT64) AS total_precipitation_mm,
    
    CAST(latitude AS FLOAT64) AS latitude,
    CAST(longitude AS FLOAT64) AS longitude,
    
    -- Metadatos de nuestro pipeline
    CAST(extraction_date AS TIMESTAMP) AS extraction_timestamp
    
FROM raw_data
-- Filtramos por si viene alguna fila corrupta sin fecha
WHERE time IS NOT NULL