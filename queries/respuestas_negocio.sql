/*
    Respuestas a las preguntas de negocio del Proyecto Integrador.
    Acá voy poniendo las queries para cada punto que pedía la consigna.
*/

-- 1. VENTAS

-- Productos más vendidos (top 10)
SELECT 
    p.product_name,
    SUM(f.quantity) as total_vendido
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_products') }} p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_vendido DESC
LIMIT 10;

-- Ticket promedio por orden
-- Agrupo primero por orden porque la fact tiene detalle por item
WITH order_totals AS (
    SELECT 
        order_id,
        SUM(total_line_amount) as monto_orden
    FROM {{ ref('fact_orders') }}
    GROUP BY order_id
)
SELECT AVG(monto_orden) as ticket_promedio FROM order_totals;

-- Categorías con más ventas
SELECT 
    p.category_name,
    SUM(f.quantity) as items_vendidos
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_products') }} p ON f.product_id = p.product_id
GROUP BY p.category_name
ORDER BY items_vendidos DESC;

-- Día de la semana con más ventas
SELECT 
    d.day_name,
    COUNT(DISTINCT f.order_id) as total_ordenes
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_date') }} d ON f.date_id = d.date_id
GROUP BY d.day_name
ORDER BY total_ordenes DESC;

-- Variación mensual de órdenes
WITH monthly_orders AS (
    SELECT 
        d.year,
        d.month,
        d.month_name,
        COUNT(DISTINCT f.order_id) as total_ordenes
    FROM {{ ref('fact_orders') }} f
    JOIN {{ ref('dim_date') }} d ON f.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
)
SELECT 
    *,
    total_ordenes - LAG(total_ordenes) OVER (ORDER BY year, month) as variacion_mensual
FROM monthly_orders;


-- 2. PAGOS Y TRANSACCIONES

-- Métodos de pago más usados
SELECT 
    pm.payment_method_name,
    COUNT(DISTINCT f.order_id) as cantidad_ordenes
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_payment_methods') }} pm ON f.payment_method_id = pm.payment_method_id
GROUP BY pm.payment_method_name
ORDER BY cantidad_ordenes DESC;

-- Recaudación total por mes
SELECT 
    d.year,
    d.month_name,
    SUM(f.total_line_amount) as recaudacion_total
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_date') }} d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- 3. USUARIOS

-- Usuarios nuevos por mes
SELECT 
    EXTRACT(YEAR FROM created_at) as anio,
    EXTRACT(MONTH FROM created_at) as mes,
    COUNT(user_id) as nuevos_usuarios
FROM {{ ref('dim_users') }}
GROUP BY 1, 2
ORDER BY 1, 2;

-- Usuarios que más gastaron (Top 10)
SELECT 
    u.first_name,
    u.last_name,
    SUM(f.total_line_amount) as total_gastado
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_users') }} u ON f.user_id = u.user_id
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY total_gastado DESC
LIMIT 10;


-- 4. PRODUCTOS Y STOCK

-- Productos con mucho stock y pocas ventas
-- Asumí que "Alto Stock" es > 50 y "Bajas Ventas" < 5 para probar
WITH ventas_producto AS (
    SELECT product_id, SUM(quantity) as total_vendido
    FROM {{ ref('fact_orders') }}
    GROUP BY product_id
)
SELECT 
    p.product_name,
    p.stock,
    COALESCE(v.total_vendido, 0) as ventas
FROM {{ ref('dim_products') }} p
LEFT JOIN ventas_producto v ON p.product_id = v.product_id
WHERE p.stock > 50 AND COALESCE(v.total_vendido, 0) < 5
ORDER BY p.stock DESC;

-- Categoría que más plata genera
SELECT 
    p.category_name,
    SUM(f.total_line_amount) as valor_total_vendido
FROM {{ ref('fact_orders') }} f
JOIN {{ ref('dim_products') }} p ON f.product_id = p.product_id
GROUP BY p.category_name
ORDER BY valor_total_vendido DESC
LIMIT 1;
