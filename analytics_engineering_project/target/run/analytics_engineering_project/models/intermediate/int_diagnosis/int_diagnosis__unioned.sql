
  
  create view "analytics_engineering_project"."main"."int_diagnosis__unioned__dbt_tmp" as (
    with unioned as (
    select * from "analytics_engineering_project"."main"."stg_payer__diagnosis"
    union all
    select * from "analytics_engineering_project"."main"."stg_ehr__diagnosis"
)

select *
from unioned
  );
