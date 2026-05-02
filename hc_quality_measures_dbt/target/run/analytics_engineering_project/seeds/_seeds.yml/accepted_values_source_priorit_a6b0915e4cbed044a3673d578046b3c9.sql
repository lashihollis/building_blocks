
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        trust_level as value_field,
        count(*) as n_records

    from "analytics_engineering_project"."main"."source_priority"
    group by trust_level

)

select *
from all_values
where value_field not in (
    'high','medium','medium_low','low'
)



  
  
      
    ) dbt_internal_test