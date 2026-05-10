with source as (
    select * from {{ source('raw', 'raw_products') }}
),

renamed as (
    select
        product_id,
        title as product_name,
        price as unit_price,
        category as product_category,
        description as product_description,
        rating_rate as avg_rating,
        rating_count as total_rating,
        loaded_at
    from source
)


select * from renamed