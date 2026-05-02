






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and vital_value >= 0 and vital_value <= 300
)
 as expression


    from "analytics_engineering_project"."main"."stg_fhir__vitals"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







