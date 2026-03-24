
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select vital_type
from "analytics_engineering_project"."main"."stg_ehr__vitals"
where vital_type is null



  
  
      
    ) dbt_internal_test