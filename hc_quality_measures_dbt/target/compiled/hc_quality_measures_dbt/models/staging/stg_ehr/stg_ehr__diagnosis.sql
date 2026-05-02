select distinct
    patient_id,
    encounter_id,
    dx_code
from "quality_measures"."main"."ehr_data"
where dx_code is not null