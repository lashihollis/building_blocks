select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'ehr' as source_system
from "analytics_engineering_project"."main"."ehr_data"
where vital_type is not null