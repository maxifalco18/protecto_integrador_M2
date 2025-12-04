{% snapshot users_snapshot %}

{{
    config(
      target_database='pi_m2_db',
      target_schema='snapshots',
      unique_key='user_id',
      strategy='check',
      check_cols=['first_name', 'last_name', 'email'],
    )
}}

select * from {{ ref('stg_users') }}

{% endsnapshot %}
