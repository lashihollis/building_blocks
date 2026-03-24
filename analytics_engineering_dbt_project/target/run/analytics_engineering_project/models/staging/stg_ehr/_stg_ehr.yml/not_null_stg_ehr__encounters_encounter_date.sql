
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select encounter_date
from "analytics_engineering_project"."main"."stg_ehr__encounters"
where encounter_date is null



  
  
      
    ) dbt_internal_test