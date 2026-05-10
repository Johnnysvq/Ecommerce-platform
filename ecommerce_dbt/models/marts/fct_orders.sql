{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

final as (
    select
        o.order_id,
        o.user_id,
        o.product_id,
        o.quantity,
        o.order_date,

        p.product_name,
        p.product_category,
        p.unit_price,
        p.avg_rating,

        u.full_name as customer_name,
        u.city as customer_city,
        u.email as customer_email,

        o.quantity * p.unit_price as total_revenue,
        o.loaded_at
    from orders o
    left join products p on o.product_id = p.product_id
    left join users u on o.user_id = u.user_id
)

select * from final