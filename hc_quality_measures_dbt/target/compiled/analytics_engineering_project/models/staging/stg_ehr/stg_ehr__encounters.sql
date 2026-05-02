select
    encounter_id,
    patient_id,
    encounter_date,
    'ehr' as source_system
from "analytics_engineering_project"."main"."ehr_data"
group by encounter_id, patient_id, encounter_date