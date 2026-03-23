
  
  create view "analytics_engineering_project"."main"."stg_ehr__encounters__dbt_tmp" as (
    select
    encounter_id,
    patient_id,
    encounter_date,
    'ehr' as source_system
from "analytics_engineering_project"."main"."ehr_data"
group by encounter_id, patient_id, encounter_date
  );
