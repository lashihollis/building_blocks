select
    encounter_id,
    patient_id,
    encounter_date,
    'payer' as source_system
from {{ source('payer', 'payer_data') }}
group by encounter_id, patient_id, encounter_date