select
    encounter_id,
    patient_id,
    encounter_date,
    'ehr' as source_system
from {{ source('ehr', 'encounters') }}
group by encounter_id, patient_id, encounter_date