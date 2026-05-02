with unioned as (
    select * from "quality_measures"."main"."stg_payer__diagnosis"
    union all
    select * from "quality_measures"."main"."stg_ehr__diagnosis"
)

select *
from unioned