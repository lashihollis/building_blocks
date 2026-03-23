with unioned as (
    select * from {{ ref('stg_payer__diagnosis') }}
    union all
    select * from {{ ref('stg_ehr__diagnosis') }}
)

select *
from unioned