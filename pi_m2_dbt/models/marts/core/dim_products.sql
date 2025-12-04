with products as (
    select * from {{ ref('stg_products') }}
),

categories as (
    select * from {{ ref('stg_categories') }}
)

select
    products.product_id,
    products.product_name,
    products.product_description,
    products.current_price,
    products.stock,
    categories.category_name,
    categories.category_description
from products
left join categories on products.category_id = categories.category_id
