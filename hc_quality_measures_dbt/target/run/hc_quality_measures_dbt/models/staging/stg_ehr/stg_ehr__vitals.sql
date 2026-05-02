
  
  create view "quality_measures"."main"."stg_ehr__vitals__dbt_tmp" as (
    select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'ehr' as source_system
from "quality_measures"."main"."ehr_data"
where vital_type is not null
  );
