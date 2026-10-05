select distinct
    patient_id,
    encounter_id,
    dx_code,
    'payer' as source_system
from {{ ref('payer_data') }}
where dx_code is not null
