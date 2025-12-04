with source as (
    select * from {{ source('raw', 'detalleordenes') }}
),

renamed as (
    select
        detalleid as order_item_id,
        ordenid as order_id,
        productoid as product_id,
        cantidad as quantity,
        preciounitario as unit_price
    from source
)

select * from renamed
