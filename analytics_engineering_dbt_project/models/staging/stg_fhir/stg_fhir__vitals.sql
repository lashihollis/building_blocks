select
    patient_id,
    cast(null as string) as encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    'fhir' as source_system
from {{ source('fhir_data', 'vitals') }}
where vital_type is not null
 