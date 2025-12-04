# Bitácora del Proyecto Integrador M2

Estado Actual: **FASE 0 - INICIO**
Rama Actual: **dev**

## FASE 0: Configuración del Entorno
- [x] Inicializar Git y conectar remoto
- [x] Crear y cambiar a rama `dev`
- [x] Crear entorno virtual Python (Usando intérprete existente)
- [x] Instalar dependencias iniciales (pandas, sqlalchemy, psycopg2, dbt-postgres)
- [x] Configurar conexión a Base de Datos (Postgres)

## FASE 1: Carga y Entendimiento
- [ ] Análisis exploratorio de archivos en `DB Proyecto`
- [ ] Creación de script de carga (Python/SQL) para capa RAW
- [ ] Ejecución de carga de datos
- [ ] Reporte de calidad de datos (Nulos, Duplicados)
- [ ] **MERGE A MAIN (Fin Fase 1)**

## FASE 2: Modelado Dimensional
- [ ] Definición de Bus Matrix (Hechos y Dimensiones)
- [ ] Diseño de Diagrama ER
- [ ] Definición de estrategias SCD
- [ ] **MERGE A MAIN (Fin Fase 2)**

## FASE 3: Implementación DBT
- [ ] Inicializar proyecto DBT
- [ ] Configurar `profiles.yml` y `sources.yml`
- [ ] Modelos Staging (Clean & Cast)
- [ ] Modelos Intermediate (Joins & Logic)
- [ ] Modelos Marts (Facts & Dims)
- [ ] **MERGE A MAIN (Fin Fase 3)**

## FASE 4: Validación y Entrega
- [ ] Implementar Tests (Generic & Singular)
- [ ] Generar Documentación DBT
- [ ] Queries SQL para responder preguntas de negocio
- [ ] **MERGE A MAIN (Fin Proyecto)**
