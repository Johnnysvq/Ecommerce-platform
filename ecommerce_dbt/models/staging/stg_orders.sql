with source as (
    select * from {{ source('raw', 'raw_orders') }}
),

renamed as (
    select
        order_id,
        user_id,
        product_id,
        quantity,
        order_date::date as order_date,
        loaded_at
    from source
)

select * from renamed