with source as (
    select * from {{ source('raw', 'ordenesmetodospago') }}
),

renamed as (
    select
        ordenid as order_id,
        metodopagoid as payment_method_id,
        montopagado as payment_amount
    from source
)

select * from renamed
