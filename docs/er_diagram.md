# Diagrama Entidad-Relación (ER) - Modelo Dimensional

Este documento detalla la estructura del esquema estrella diseñado para el Data Warehouse.

## Esquema Estrella

El modelo centraliza las métricas de negocio en la tabla de hechos `fact_orders` y rodea esta tabla con dimensiones descriptivas.

```mermaid
erDiagram
    %% Fact Table
    fact_orders {
        int order_item_sk PK
        int order_id
        int user_sk FK
        int product_sk FK
        int payment_method_sk FK
        int date_sk FK
        int cantidad
        decimal precio_unitario
        decimal total_linea
    }

    %% Dimensions
    dim_users {
        int user_sk PK
        int user_id_nk
        string nombre
        string apellido
        string email
        string telefono
        string direccion
        string ciudad
        string provincia
        string codigo_postal
    }

    dim_products {
        int product_sk PK
        int product_id_nk
        string nombre_producto
        decimal precio_actual
        string categoria_nombre
    }

    dim_payment_methods {
        int payment_method_sk PK
        int payment_method_id_nk
        string nombre_metodo
    }

    dim_date {
        int date_sk PK
        date fecha_completa
        int anio
        int mes
        int dia
        int dia_semana
        string nombre_dia
        string nombre_mes
        boolean es_fin_de_semana
    }

    %% Relationships
    fact_orders }|..|| dim_users : "FK_user"
    fact_orders }|..|| dim_products : "FK_product"
    fact_orders }|..|| dim_payment_methods : "FK_payment"
    fact_orders }|..|| dim_date : "FK_date"
```

## Diccionario de Datos

### Claves Surrogadas (SK) vs Claves Naturales (NK)
- **SK (Surrogate Key)**: Claves primarias generadas por el Data Warehouse (generalmente enteros autoincrementales o hashes). Se usan para unir las tablas de hechos con las dimensiones. Permiten manejar historia (SCD Tipo 2) sin romper la integridad referencial.
- **NK (Natural Key)**: Claves originales del sistema fuente (ej. `id` en la tabla `usuarios`). Se mantienen en la dimensión para trazabilidad y búsquedas.

### Cardinalidad
- Todas las relaciones son de **Uno a Muchos** desde la Dimensión hacia la Fact Table.
- Una orden puede tener múltiples productos, por lo que la granularidad de `fact_orders` es a nivel de **línea de orden** (producto dentro de una orden).
