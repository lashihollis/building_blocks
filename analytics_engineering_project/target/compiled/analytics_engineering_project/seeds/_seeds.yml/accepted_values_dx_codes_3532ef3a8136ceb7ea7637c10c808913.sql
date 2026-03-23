
    
    

with all_values as (

    select
        condition_category as value_field,
        count(*) as n_records

    from "analytics_engineering_project"."main"."dx_codes"
    group by condition_category

)

select *
from all_values
where value_field not in (
    'hypertension','diabetes'
)


