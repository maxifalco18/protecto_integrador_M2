with products_snapshot as (
    select * from {{ ref('products_snapshot') }}
),

categories as (
    select * from {{ ref('stg_categories') }}
)

select
    products_snapshot.product_id,
    products_snapshot.product_name,
    products_snapshot.product_description,
    products_snapshot.current_price,
    products_snapshot.stock,
    categories.category_name,
    categories.category_description,
    products_snapshot.dbt_valid_from,
    products_snapshot.dbt_valid_to,
    products_snapshot.dbt_scd_id,
    products_snapshot.dbt_updated_at
from products_snapshot
left join categories on products_snapshot.category_id = categories.category_id
