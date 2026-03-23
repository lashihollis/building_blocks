with unioned as (

select * 
from "analytics_engineering_project"."main"."int_vitals__unioned"

),

ranked as (
    select
        *,
        row_number() over (
            partition by patient_id, vital_date, vital_type
            order by
                case source_system
                    when 'payer' then 1
                    when 'ehr' then 2
                    when 'patient_reported' then 3
                end
        ) as rank
    from unioned
)

select *
from ranked
where rank = 1