
  
  create view "analytics_engineering_project"."main"."int_vitals__unioned__dbt_tmp" as (
    with unioned as (
    select * from "analytics_engineering_project"."main"."stg_payer__vitals"
    union all
    select * from "analytics_engineering_project"."main"."stg_ehr__vitals"
    union all
    select * from "analytics_engineering_project"."main"."stg_patient_reported__vitals"
)

select *
from unioned
  );
