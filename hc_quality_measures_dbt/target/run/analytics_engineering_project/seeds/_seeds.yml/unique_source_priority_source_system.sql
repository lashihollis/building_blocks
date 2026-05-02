
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    source_system as unique_field,
    count(*) as n_records

from "analytics_engineering_project"."main"."source_priority"
where source_system is not null
group by source_system
having count(*) > 1



  
  
      
    ) dbt_internal_test