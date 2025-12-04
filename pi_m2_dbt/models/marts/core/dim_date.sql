with orders as (
    select * from {{ ref('stg_orders') }}
),

date_range as (
    select
        min(order_date::date) as min_date,
        max(order_date::date) as max_date
    from orders
),

date_spine as (
    select
        generate_series(
            min_date,
            max_date,
            '1 day'::interval
        )::date as date_day
    from date_range
)

select
    to_char(date_day, 'YYYYMMDD')::int as date_id,
    date_day as full_date,
    extract(year from date_day)::int as year,
    extract(month from date_day)::int as month,
    extract(day from date_day)::int as day,
    extract(dow from date_day)::int as day_of_week,
    to_char(date_day, 'Day') as day_name,
    to_char(date_day, 'Month') as month_name,
    extract(quarter from date_day)::int as quarter,
    case when extract(dow from date_day) in (0, 6) then true else false end as is_weekend
from date_spine
