
  
  create view "quality_measures"."main"."int_diagnosis__unioned__dbt_tmp" as (
    with unioned as (
    select * from "quality_measures"."main"."stg_payer__diagnosis"
    union all
    select * from "quality_measures"."main"."stg_ehr__diagnosis"
)

select *
from unioned
  );
