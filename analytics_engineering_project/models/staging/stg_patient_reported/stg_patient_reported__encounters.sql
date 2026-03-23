select
    encounter_id,
    patient_id,
    encounter_date,
    'patient_reported' as source_system
from {{ source('patient_reported', 'patient_reported_data') }}
group by encounter_id, patient_id, encounter_date