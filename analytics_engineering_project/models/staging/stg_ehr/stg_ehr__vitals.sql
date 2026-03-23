select
    patient_id,
    encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'ehr' as source_system
from {{ source('ehr', 'ehr_data') }}
where vital_type is not null
