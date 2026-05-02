
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select vital_date
from "analytics_engineering_project"."main"."patient_reported_data"
where vital_date is null



  
  
      
    ) dbt_internal_test