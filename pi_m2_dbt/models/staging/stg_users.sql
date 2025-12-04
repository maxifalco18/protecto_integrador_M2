with source as (
    select * from {{ source('raw', 'usuarios') }}
),

renamed as (
    select
        usuarioid as user_id,
        nombre as first_name,
        apellido as last_name,
        dni,
        email,
        fecharegistro as created_at
    from source
)

select * from renamed
