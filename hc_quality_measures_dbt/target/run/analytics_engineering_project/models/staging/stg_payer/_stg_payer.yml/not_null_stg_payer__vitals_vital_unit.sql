
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select vital_unit
from "analytics_engineering_project"."main"."stg_payer__vitals"
where vital_unit is null



  
  
      
    ) dbt_internal_test