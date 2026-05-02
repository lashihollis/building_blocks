
  
  create view "quality_measures"."main"."int_vitals__unioned__dbt_tmp" as (
    with unioned as (
    select * from "quality_measures"."main"."stg_payer__vitals"
    union all
    select * from "quality_measures"."main"."stg_ehr__vitals"
    union all
    select * from "quality_measures"."main"."stg_patient_reported__vitals"
)

select *
from unioned
  );
