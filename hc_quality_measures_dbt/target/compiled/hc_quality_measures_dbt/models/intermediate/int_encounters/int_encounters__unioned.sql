with unioned as (
    select * from "quality_measures"."main"."stg_payer__encounters"
    union all
    select * from "quality_measures"."main"."stg_ehr__encounters"
)

select *
from unioned