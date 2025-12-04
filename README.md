# Proyecto Integrador M2 - Data Engineering 🚀

Este repositorio contiene la solución completa al Proyecto Integrador del Módulo 2 de la carrera de Data Engineering en Henry.

El objetivo fue construir un **Data Warehouse** para una plataforma de E-commerce, partiendo de archivos CSV crudos, pasando por un proceso de ingesta, limpieza y transformación, hasta llegar a un modelo dimensional (Estrella) listo para ser consumido por herramientas de BI.

## 🛠️ Tecnologías Utilizadas
- **Python**: Para la ingesta de datos y scripts de control.
- **PostgreSQL**: Como motor de base de datos (Data Warehouse).
- **dbt (data build tool)**: Para la transformación de datos, testing y documentación.
- **SQL**: Para consultas de negocio y definiciones DDL.

## 📂 Estructura del Proyecto
- `DB Proyecto/`: Archivos fuente (CSVs) y scripts SQL originales.
- `pi_m2_dbt/`: Directorio principal del proyecto dbt.
  - `models/staging`: Capa de limpieza y estandarización (Vistas).
  - `models/intermediate`: Lógica de negocio y pre-joins.
  - `models/marts`: Tablas de Hechos y Dimensiones finales.
  - `snapshots`: **SCD Tipo 2** para historizar cambios en Usuarios y Productos.
- `queries/`: Respuestas SQL a las preguntas de negocio planteadas.
- `docs/`: Documentación de diseño (Bus Matrix, Diagrama ER).
- `scripts/`: Scripts auxiliares (Carga inicial, EDA).

## ⚙️ Configuración y Ejecución

### 1. Prerrequisitos
Tener instalado Python 3.x, PostgreSQL y Git.

### 2. Configuración del Entorno
1. Clonar el repositorio.
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar variables de entorno:
   Crear un archivo `.env` en la raíz (basado en el ejemplo) con las credenciales de la base de datos para que funcionen los scripts de carga.

### 3. Carga de Datos (Ingesta)
Si la base de datos está vacía, ejecutar el script de carga inicial:
```bash
python scripts/load_raw_data.py
```
*Esto leerá los CSVs de `DB Proyecto/csv` y poblará las tablas raw en Postgres.*

### 4. Transformación con dbt
Navegar a la carpeta del proyecto dbt:
```bash
cd pi_m2_dbt
```

Ejecutar los siguientes comandos en orden:
```bash
# Instalar dependencias (si las hubiera)
dbt deps

# Crear los snapshots (Importante para SCD Tipo 2)
dbt snapshot

# Correr los modelos (Staging -> Intermediate -> Marts)
dbt run

# Ejecutar los tests de calidad de datos
dbt test
```

### 5. Documentación
Para ver el linaje de datos y la documentación generada:
```bash
dbt docs generate
dbt docs serve
```

## 📝 Notas de Diseño
- **SCD Tipo 2**: Decidí implementar *Slowly Changing Dimensions* Tipo 2 para las dimensiones de `Usuarios` y `Productos`. Esto permite analizar cómo cambian los atributos (como precios o direcciones) a lo largo del tiempo sin perder la historia.
- **Testing**: Se agregaron tests de unicidad (`unique`), no nulos (`not_null`) e integridad referencial (`relationships`) para asegurar la calidad de los datos en la capa final.

---
*Proyecto realizado por [Tu Nombre] para Henry.*
