with source as (
    select * from {{ source('raw', 'productos') }}
),

renamed as (
    select
        productoid as product_id,
        nombre as product_name,
        descripcion as product_description,
        precio as current_price,
        stock,
        categoriaid as category_id
    from source
)

select * from renamed
