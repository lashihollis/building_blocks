
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select priority_rank
from "analytics_engineering_project"."main"."source_priority"
where priority_rank is null



  
  
      
    ) dbt_internal_test