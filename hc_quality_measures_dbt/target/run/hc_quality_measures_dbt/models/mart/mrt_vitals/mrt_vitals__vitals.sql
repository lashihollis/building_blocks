
  
  create view "quality_measures"."main"."mrt_vitals__vitals__dbt_tmp" as (
    select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    source_system
from "quality_measures"."main"."int_vitals__ranked"
  );
