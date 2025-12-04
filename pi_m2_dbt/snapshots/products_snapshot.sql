{% snapshot products_snapshot %}

{{
    config(
      target_database='pi_m2_db',
      target_schema='snapshots',
      unique_key='product_id',
      strategy='check',
      check_cols=['current_price', 'stock', 'category_id'],
    )
}}

select * from {{ ref('stg_products') }}

{% endsnapshot %}
