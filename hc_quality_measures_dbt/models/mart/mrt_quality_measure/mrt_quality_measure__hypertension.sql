with hypertension_patients as (
    select distinct
        d.patient_id
    from {{ ref('int_diagnosis__unioned') }} as d
    inner join {{ ref('dx_codes') }} as dx
        on d.dx_code = dx.dx_code
    where dx.condition_category = 'hypertension'
),

measure_as_of_date as (
    select current_date as measure_as_of_date
),

bp_checks as (
    select
        vitals.patient_id,
        max(vital_date) as most_recent_bp_date
    from {{ ref('mrt_vitals__vitals') }} as vitals
    cross join measure_as_of_date
    where vital_type in ('BP_SYSTOLIC', 'BP_DIASTOLIC')
        and vital_date <= measure_as_of_date.measure_as_of_date
    group by vitals.patient_id
)

select
    h.patient_id,
    b.most_recent_bp_date,
    measure_as_of_date.measure_as_of_date,
    case
        when b.most_recent_bp_date between
            measure_as_of_date.measure_as_of_date - interval '6 months'
            and measure_as_of_date.measure_as_of_date
            then 1
        else 0
    end as compliant
from hypertension_patients h
left join bp_checks b
    on h.patient_id = b.patient_id
cross join measure_as_of_date