with order_items as (
    select * from {{ ref('int_order_items_enriched') }}
),

orders as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    -- Surrogate Keys (Generated usually, but using IDs for simplicity here or could use dbt_utils.generate_surrogate_key)
    order_items.order_item_id,
    
    -- Foreign Keys
    orders.user_id,
    order_items.product_id,
    orders.payment_method_id,
    to_char(orders.order_date::date, 'YYYYMMDD')::int as date_id,
    
    -- Degenerate Dimensions
    orders.order_id,
    orders.order_status,
    
    -- Metrics
    order_items.quantity,
    order_items.unit_price,
    order_items.total_line_amount,
    
    -- Metadata
    orders.order_date as created_at

from order_items
join orders on order_items.order_id = orders.order_id
