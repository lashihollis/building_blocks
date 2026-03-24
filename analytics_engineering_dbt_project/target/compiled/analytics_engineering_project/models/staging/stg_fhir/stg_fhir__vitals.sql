select
    patient_id,
    cast(null as string) as encounter_id,
    vital_date,
    vital_type,
    vital_value,
    vital_unit,
    source_system
from "fhir_data"."main"."vitals"
where vital_type is not null