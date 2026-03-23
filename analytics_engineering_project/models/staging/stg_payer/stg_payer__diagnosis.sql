select distinct
    patient_id,
    encounter_id,
    dx_code
from {{ source('payer', 'payer_data') }}
where dx_code is not null
