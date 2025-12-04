with source as (
    select * from {{ source('raw', 'ordenes') }}
),

renamed as (
    select
        ordenid as order_id,
        usuarioid as user_id,
        fechaorden as order_date,
        total as order_total,
        estado as order_status
    from source
)

select * from renamed
