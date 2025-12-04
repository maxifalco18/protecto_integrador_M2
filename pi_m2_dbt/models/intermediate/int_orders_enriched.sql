with orders as (
    select * from {{ ref('stg_orders') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

payments as (
    select * from {{ ref('stg_order_payments') }}
),

-- Lógica para asignar un único método de pago principal por orden (el de mayor monto)
primary_payment as (
    select distinct on (order_id)
        order_id,
        payment_method_id
    from payments
    order by order_id, payment_amount desc
)

select
    orders.order_id,
    orders.user_id,
    orders.order_date,
    orders.order_total,
    orders.order_status,
    users.first_name,
    users.last_name,
    users.email,
    coalesce(primary_payment.payment_method_id, 1) as payment_method_id -- Default a 1 (Efectivo/Otro) si no hay pago registrado
from orders
left join users on orders.user_id = users.user_id
left join primary_payment on orders.order_id = primary_payment.order_id
