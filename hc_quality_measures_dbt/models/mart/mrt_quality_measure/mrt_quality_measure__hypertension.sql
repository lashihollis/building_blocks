with hypertension_patients as (
    select distinct
        d.patient_id
    from {{ ref('int_diagnosis__unioned') }} d
    inner join {{ ref('dx_codes') }} dx
        on d.dx_code = dx.dx_code
    where dx.dx_code in ('I10', 'I11', 'I12', 'I13', 'I15') -- ICD-10 codes for hypertension
),

bp_checks as (
    select
        patient_id,
        max(vital_date) as most_recent_bp_date
    from {{ ref('mrt_vitals__vitals') }}
    where vital_type in ('BP_SYSTOLIC', 'BP_DIASTOLIC')
    group by patient_id
)

select
    h.patient_id,
    b.most_recent_bp_date,
    case
        --data is synthesized based on years 2023 and 2024
        when b.most_recent_bp_date >= (CURRENT_DATE - interval '180 days') then 1 
        else 0
    end as compliant
from hypertension_patients h
left join bp_checks b
    on h.patient_id = b.patient_id