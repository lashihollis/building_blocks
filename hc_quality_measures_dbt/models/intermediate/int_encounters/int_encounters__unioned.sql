with unioned as (
    select * from {{ ref('stg_payer__encounters') }}
    union all
    select * from {{ ref('stg_ehr__encounters') }}
)

select *
from unioned
