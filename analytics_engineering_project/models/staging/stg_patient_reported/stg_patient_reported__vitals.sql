select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'patient_reported' as source_system
from {{ source('patient_reported', 'patient_reported_data') }}
where vital_type is not null
