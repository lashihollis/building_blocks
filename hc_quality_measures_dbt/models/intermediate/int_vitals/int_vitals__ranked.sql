with ranked as (
    select
        vitals.patient_id,
        vitals.encounter_id,
        vitals.vital_date,
        vitals.vital_type,
        vitals.vital_value,
        vitals.vital_unit,
        vitals.source_system,
        source_priority.priority_rank as source_priority_rank,
        row_number() over (
            partition by
                vitals.patient_id,
                vitals.vital_date,
                vitals.vital_type
            order by
                source_priority.priority_rank,
                vitals.encounter_id nulls last,
                vitals.vital_value,
                vitals.vital_unit
        ) as source_rank
    from {{ ref('int_vitals__unioned') }} as vitals
    left join {{ ref('source_priority') }} as source_priority
        on vitals.source_system = source_priority.source_system
)

select *
from ranked