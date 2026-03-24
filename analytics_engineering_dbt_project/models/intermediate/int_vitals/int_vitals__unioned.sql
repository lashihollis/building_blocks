with unioned as (
    select * from {{ ref('stg_payer__vitals') }}
    union all
    select * from {{ ref('stg_ehr__vitals') }}
    union all
    select * from {{ ref('stg_patient_reported__vitals') }}
    union all
    select * from {{ ref('stg_fhir__vitals') }}
)

select *
from unioned
