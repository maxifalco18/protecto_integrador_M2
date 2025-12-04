# Bitácora de Trabajo - Proyecto Integrador M2

## Configuración Inicial

Empecé configurando el entorno. Tuve que instalar varias librerías de Python (`pandas`, `sqlalchemy`, `psycopg2`) y configurar `dbt-postgres`.
Al principio me dio un error la conexión a la base de datos local, pero revisé el puerto y el usuario y pude conectar.
Ya dejé creada la rama `dev` para ir trabajando ahí.

## Fase 1: Carga de Datos (Ingesta)

Hice un análisis rápido de los CSVs que nos pasaron.

- Creé un script en Python para cargar todo a la base de datos (capa RAW).
- Chequeé nulos y duplicados. Parece que la data viene bastante limpia, pero igual hay que tener cuidado con las fechas.
- Hice el merge a main de esta parte.

## Fase 2: Modelado

Estuve diseñando el modelo dimensional.

- Definí la Bus Matrix para tener claro cuáles son los hechos y dimensiones.
- Armé el diagrama ER.
- **Decisión importante:** Para los usuarios y productos voy a usar SCD Tipo 2 porque nos piden trackear cambios históricos (precios, direcciones, etc).

## Fase 3: DBT

Acá es donde más tiempo invertí.

- Inicialicé el proyecto dbt.
- Configure `profiles.yml`.
- **Staging:** Limpié los nombres de columnas y casteé tipos de datos.
- **Intermediate:** Hice algunos joins previos para enriquecer las órdenes.
- **Snapshots:** Implementé los snapshots para `users` y `products`. Tuve que leer la docu de dbt para configurar bien la estrategia `check`.
- **Marts:** Armé la fact table `fact_orders` y las dimensiones.
- Corregí un tema con la dimensión de usuarios para que lea del snapshot y no del staging directo.

## Fase 4: Validación

- Agregué tests en el `schema.yml` (not null, unique y foreign keys).
- Escribí las queries para responder las preguntas de negocio que pedía la consigna.
- Generé la documentación con `dbt docs generate`.
- Todo listo para entregar. Hice el merge final a main.

## Conclusión

El proyecto quedó completo. Lo que más me costó fue entender bien cómo conectar los snapshots con las dimensiones, pero creo que quedó sólido. La estructura de carpetas de dbt ayuda mucho a mantener el orden.
