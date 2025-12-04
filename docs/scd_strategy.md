# Estrategias de Slowly Changing Dimensions (SCD)

Este documento define cómo se manejarán los cambios en los datos de las dimensiones a lo largo del tiempo.

## Definiciones
- **SCD Tipo 0 (Fixed)**: El dato nunca cambia una vez insertado.
- **SCD Tipo 1 (Overwrite)**: Se sobrescribe el valor antiguo con el nuevo. No se guarda historia.
- **SCD Tipo 2 (Add Row)**: Se crea una nueva fila para el registro con los nuevos valores, preservando la fila anterior. Se usan columnas de vigencia (`valid_from`, `valid_to`, `is_current`).

## Estrategia por Dimensión

### 1. `dim_users`
Los usuarios pueden cambiar de domicilio. Para análisis geoespacial histórico, es crucial saber dónde vivía el usuario en el momento de cada compra.

| Atributo | Tipo SCD | Justificación |
| :--- | :--- | :--- |
| `user_id` (NK) | - | Clave Natural (Inmutable) |
| `nombre`, `apellido` | **Tipo 1** | Corrección de errores tipográficos. No aporta valor analítico guardar historia de cambios de nombre. |
| `email`, `telefono` | **Tipo 1** | Datos de contacto actuales. |
| `direccion`, `ciudad`, `provincia` | **Tipo 2** | **Crítico**. Si un usuario se muda, las ventas históricas deben seguir asociadas a su ubicación original. |

**Columnas de Auditoría requeridas**: `dbt_valid_from`, `dbt_valid_to`, `dbt_scd_id`, `dbt_updated_at`.

### 2. `dim_products`
Los productos pueden cambiar de precio o de categoría.

| Atributo | Tipo SCD | Justificación |
| :--- | :--- | :--- |
| `product_id` (NK) | - | Clave Natural |
| `nombre_producto` | **Tipo 1** | Corrección de nombres. |
| `precio_actual` | **Tipo 2** | Permite analizar la evolución del precio de lista del producto en el tiempo (independiente del precio de venta real en la Fact). |
| `categoria` | **Tipo 2** | Si un producto se recategoriza, queremos mantener la historia de cómo se clasificaba antes. |

### 3. `dim_payment_methods`
Tabla pequeña y muy estable.

| Atributo | Tipo SCD | Justificación |
| :--- | :--- | :--- |
| `payment_method_id` (NK) | - | Clave Natural |
| `nombre_metodo` | **Tipo 1** | Solo correcciones de texto. |

### 4. `dim_date`
**Tipo 0**. La dimensión de tiempo es estática y se genera una sola vez.

## Implementación en dbt
Utilizaremos la funcionalidad de **Snapshots** de dbt para implementar SCD Tipo 2.
- **Strategy**: `timestamp` (usando `updated_at` de la fuente si existe) o `check` (comparando hash de columnas).
- Dado que nuestros CSVs son estáticos por ahora, simularemos la carga inicial. En un entorno real, los snapshots detectarían cambios en cargas incrementales.
