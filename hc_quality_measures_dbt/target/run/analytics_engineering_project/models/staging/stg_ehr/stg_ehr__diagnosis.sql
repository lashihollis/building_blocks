
  
  create view "analytics_engineering_project"."main"."stg_ehr__diagnosis__dbt_tmp" as (
    select distinct
    patient_id,
    encounter_id,
    dx_code
from "analytics_engineering_project"."main"."ehr_data"
where dx_code is not null
  );
