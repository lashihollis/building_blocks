
  
  create view "analytics_engineering_project"."main"."stg_payer__vitals__dbt_tmp" as (
    select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'payer' as source_system
from "analytics_engineering_project"."main"."payer_data"
where vital_type is not null
  );
