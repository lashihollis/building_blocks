
  
  create view "analytics_engineering_project"."main"."int_encounters__unioned__dbt_tmp" as (
    with unioned as (
    select * from "analytics_engineering_project"."main"."stg_payer__encounters"
    union all
    select * from "analytics_engineering_project"."main"."stg_ehr__encounters"
)

select *
from unioned
  );
