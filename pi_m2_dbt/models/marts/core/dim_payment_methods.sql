with payment_methods as (
    select * from {{ ref('stg_payment_methods') }}
)

select
    payment_method_id,
    payment_method_name,
    payment_method_description
from payment_methods
