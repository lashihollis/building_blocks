
  
  create view "analytics_engineering_project"."main"."stg_payer__encounters__dbt_tmp" as (
    select
    encounter_id,
    patient_id,
    encounter_date,
    'payer' as source_system
from "analytics_engineering_project"."main"."payer_data"
group by encounter_id, patient_id, encounter_date
  );
