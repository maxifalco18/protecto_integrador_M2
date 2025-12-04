with source as (
    select * from {{ source('raw', 'metodospago') }}
),

renamed as (
    select
        metodopagoid as payment_method_id,
        nombre as payment_method_name,
        descripcion as payment_method_description
    from source
)

select * from renamed
