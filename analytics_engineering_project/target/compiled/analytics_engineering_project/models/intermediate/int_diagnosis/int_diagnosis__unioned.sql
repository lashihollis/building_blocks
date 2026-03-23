with unioned as (
    select * from "analytics_engineering_project"."main"."stg_payer__diagnosis"
    union all
    select * from "analytics_engineering_project"."main"."stg_ehr__diagnosis"
)

select *
from unioned