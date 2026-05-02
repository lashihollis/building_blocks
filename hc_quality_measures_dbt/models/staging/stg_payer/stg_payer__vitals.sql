select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'payer' as source_system
from {{ ref('payer_data') }}
where vital_type is not null
