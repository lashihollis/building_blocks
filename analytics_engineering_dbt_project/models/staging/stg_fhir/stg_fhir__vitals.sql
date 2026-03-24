select
    patient_id,
    string(null) as encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    source_system
from {{ source('fhir_data', 'vitals') }}
where vital_type is not null
