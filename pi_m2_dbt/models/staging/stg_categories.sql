with source as (
    select * from {{ source('raw', 'categorias') }}
),

renamed as (
    select
        categoriaid as category_id,
        nombre as category_name,
        descripcion as category_description
    from source
)

select * from renamed
