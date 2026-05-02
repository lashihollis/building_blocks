
  
  create view "analytics_engineering_project"."main"."stg_patient_reported__vitals__dbt_tmp" as (
    select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'patient_reported' as source_system
from "analytics_engineering_project"."main"."patient_reported_data"
where vital_type is not null
  );
