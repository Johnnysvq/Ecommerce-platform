{{ config(materialized='table') }}

with products as (
    select * from {{ ref('stg_products') }}
),

final as (
    select
        product_id,
        product_name,
        product_category,
        unit_price,
        avg_rating,
        total_rating,
        product_description,

        -- Clasificacion de precio
        case
            when unit_price < 20 then 'budget'
            when unit_price < 100 then 'mid-range'
            else 'premium'
        end as price_tier

    from products
)

select * from final