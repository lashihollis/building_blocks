
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select vital_value
from "analytics_engineering_project"."main"."stg_patient_reported__vitals"
where vital_value is null



  
  
      
    ) dbt_internal_test