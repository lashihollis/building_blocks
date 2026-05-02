
  
  create view "analytics_engineering_project"."main"."mrt_vitals__vitals__dbt_tmp" as (
    select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    source_system
from "analytics_engineering_project"."main"."int_vitals__ranked"
  );
