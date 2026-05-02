
  
  create view "quality_measures"."main"."stg_payer__diagnosis__dbt_tmp" as (
    select distinct
    patient_id,
    encounter_id,
    dx_code
from "quality_measures"."main"."payer_data"
where dx_code is not null
  );
