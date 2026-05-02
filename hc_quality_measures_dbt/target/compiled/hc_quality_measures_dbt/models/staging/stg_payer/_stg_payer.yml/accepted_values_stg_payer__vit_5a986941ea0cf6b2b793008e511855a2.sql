
    
    

with all_values as (

    select
        vital_type as value_field,
        count(*) as n_records

    from "quality_measures"."main"."stg_payer__vitals"
    group by vital_type

)

select *
from all_values
where value_field not in (
    'BP_SYSTOLIC','BP_DIASTOLIC'
)


