-- Le indicamos a dbt que queremos crear una Tabla física en BigQuery, no una Vista
{{ config(materialized='table') }}

WITH staging_weather AS (
    -- Usamos ref() para leer de nuestro modelo de dbt, ¡ya no de la tabla cruda!
    SELECT * FROM {{ ref('stg_weather') }}
),

daily_metrics AS (
    SELECT
        observation_date,
        -- Calculamos una temperatura media aproximada por día
        (max_temperature_c + min_temperature_c) / 2.0 AS avg_daily_temp,
        total_precipitation_mm
    FROM staging_weather
),

monthly_metrics AS (
    SELECT
        EXTRACT(YEAR FROM observation_date) AS observation_year,
        EXTRACT(MONTH FROM observation_date) AS observation_month,
        
        -- Agregaciones principales del mes
        AVG(avg_daily_temp) AS avg_monthly_temperature,
        
        -- Días de lluvia (contamos los días donde llovió más de 0 mm)
        COUNTIF(total_precipitation_mm > 0) AS rainy_days
        
    FROM daily_metrics
    GROUP BY 1, 2
)

SELECT
    observation_year,
    observation_month,
    avg_monthly_temperature,
    rainy_days,
    
    -- Cálculo de anomalía: Diferencia entre la temperatura de este mes y el promedio histórico total
    avg_monthly_temperature - AVG(avg_monthly_temperature) OVER () AS temperature_anomaly
    
FROM monthly_metrics
ORDER BY observation_year DESC, observation_month DESC