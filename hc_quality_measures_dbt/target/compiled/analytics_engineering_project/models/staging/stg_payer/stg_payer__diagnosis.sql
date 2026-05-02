select distinct
    patient_id,
    encounter_id,
    dx_code
from "analytics_engineering_project"."main"."payer_data"
where dx_code is not null