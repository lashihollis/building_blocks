
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    dx_code as unique_field,
    count(*) as n_records

from "analytics_engineering_project"."main"."dx_codes"
where dx_code is not null
group by dx_code
having count(*) > 1



  
  
      
    ) dbt_internal_test