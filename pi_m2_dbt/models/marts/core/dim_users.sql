with users_snapshot as (
    select * from {{ ref('users_snapshot') }}
)

select
    user_id,
    first_name,
    last_name,
    email,
    created_at,
    dbt_valid_from,
    dbt_valid_to,
    dbt_scd_id,
    dbt_updated_at
from users_snapshot
