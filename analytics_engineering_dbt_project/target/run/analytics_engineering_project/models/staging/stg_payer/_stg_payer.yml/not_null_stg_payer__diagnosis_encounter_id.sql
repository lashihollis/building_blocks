
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select encounter_id
from "analytics_engineering_project"."main"."stg_payer__diagnosis"
where encounter_id is null



  
  
      
    ) dbt_internal_test