
    
    

with all_values as (

    select
        vital_type as value_field,
        count(*) as n_records

    from "analytics_engineering_project"."main"."stg_patient_reported__vitals"
    group by vital_type

)

select *
from all_values
where value_field not in (
    'BP_SYSTOLIC','BP_DIASTOLIC'
)


