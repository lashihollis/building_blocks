
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select dx_code
from "quality_measures"."main"."stg_payer__diagnosis"
where dx_code is null



  
  
      
    ) dbt_internal_test