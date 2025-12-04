with items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

categories as (
    select * from {{ ref('stg_categories') }}
)

select
    items.order_item_id,
    items.order_id,
    items.product_id,
    items.quantity,
    items.unit_price,
    (items.quantity * items.unit_price) as total_line_amount,
    products.product_name,
    products.category_id,
    categories.category_name
from items
left join products on items.product_id = products.product_id
left join categories on products.category_id = categories.category_id
