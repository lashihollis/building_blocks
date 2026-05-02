
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select dx_code
from "analytics_engineering_project"."main"."dx_codes"
where dx_code is null



  
  
      
    ) dbt_internal_test