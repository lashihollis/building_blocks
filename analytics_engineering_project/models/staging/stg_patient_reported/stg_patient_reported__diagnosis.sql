select distinct
    patient_id,
    encounter_id,
    dx_code
from {{ source('patient_reported', 'patient_reported_data') }}
where dx_code is not null