with source as (
    select * from {{ source('raw', 'raw_users') }}
),

renamed as (
    select
        user_id,
        first_name,
        last_name,
        full_name,
        email,
        city,
        loaded_at
    from source
)

select * from renamed