# Bitácora del Proyecto Integrador M2

Estado Actual: **FASE 2 - MODELADO**
Rama Actual: **dev**

## FASE 0: Configuración del Entorno
- [x] Inicializar Git y conectar remoto
- [x] Crear y cambiar a rama `dev`
- [x] Crear entorno virtual Python (Usando intérprete existente)
- [x] Instalar dependencias iniciales (pandas, sqlalchemy, psycopg2, dbt-postgres)
- [x] Configurar conexión a Base de Datos (Postgres)

## FASE 1: Carga y Entendimiento
- [x] Análisis exploratorio de archivos en `DB Proyecto`
- [x] Creación de script de carga (Python/SQL) para capa RAW
- [x] Ejecución de carga de datos
- [x] Reporte de calidad de datos (Nulos, Duplicados)
- [x] **MERGE A MAIN (Fin Fase 1)**

## FASE 2: Modelado Dimensional
- [x] Definición de Bus Matrix (Hechos y Dimensiones)
- [x] Diseño de Diagrama ER
- [x] Definición de estrategias SCD
- [x] **MERGE A MAIN (Fin Fase 2)**

## FASE 3: Implementación DBT
- [x] Inicializar proyecto DBT
- [x] Configurar `profiles.yml` y `sources.yml`
- [x] Modelos Staging (Clean & Cast)
- [x] Modelos Intermediate (Joins & Logic)
- [x] Implementación de Snapshots (SCD Tipo 2)
- [x] Modelos Marts (Facts & Dims)
- [x] **MERGE A MAIN (Fin Fase 3)**

## FASE 4: Validación y Entrega
- [x] Implementar Tests (Generic & Singular)
- [x] Queries SQL para responder preguntas de negocio
- [x] Generar Documentación DBT
- [x] **MERGE A MAIN (Fin Proyecto)**
