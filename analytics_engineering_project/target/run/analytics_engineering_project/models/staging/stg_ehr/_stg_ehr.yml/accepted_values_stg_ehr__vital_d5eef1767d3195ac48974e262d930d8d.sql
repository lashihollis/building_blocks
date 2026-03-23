
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        vital_type as value_field,
        count(*) as n_records

    from "analytics_engineering_project"."main"."stg_ehr__vitals"
    group by vital_type

)

select *
from all_values
where value_field not in (
    'BP_SYSTOLIC','BP_DIASTOLIC'
)



  
  
      
    ) dbt_internal_test