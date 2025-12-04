# Proyecto Integrador M2 - Data Engineering

Este repositorio contiene la solución al Proyecto Integrador del Módulo 2.

## Estructura del Proyecto
- `DB Proyecto/`: Contiene los archivos CSV originales y los scripts SQL de las tablas raw.
- `pi_m2_dbt/`: Proyecto dbt con toda la lógica de transformación.
  - `models/staging`: Limpieza inicial.
  - `models/intermediate`: Enriquecimiento de datos.
  - `models/marts`: Modelo dimensional (Facts y Dimensions).
  - `snapshots`: Implementación de SCD Tipo 2 para usuarios y productos.
- `queries/`: Scripts SQL con las respuestas a las preguntas de negocio.
- `scripts/`: Scripts de Python para la carga inicial y chequeos.

## Cómo correr el proyecto

1. **Levantar el entorno:**
   Asegurate de tener el entorno virtual activado y las dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. **Cargar los datos (si la base está vacía):**
   ```bash
   python scripts/load_raw_data.py
   ```

3. **Ejecutar dbt:**
   Entrar a la carpeta del proyecto dbt:
   ```bash
   cd pi_m2_dbt
   ```
   Correr los modelos y snapshots:
   ```bash
   dbt deps
   dbt snapshot
   dbt run
   ```

4. **Testear:**
   ```bash
   dbt test
   ```

5. **Ver la documentación:**
   ```bash
   dbt docs generate
   dbt docs serve
   ```

## Notas
- Usé **SCD Tipo 2** para `dim_users` y `dim_products` porque me pareció lo más correcto para no perder historia de cambios.
- Las respuestas de negocio están en `queries/respuestas_negocio.sql`.
