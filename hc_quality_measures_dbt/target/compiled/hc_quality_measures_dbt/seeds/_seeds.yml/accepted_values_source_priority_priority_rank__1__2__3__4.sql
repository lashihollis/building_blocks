
    
    

with all_values as (

    select
        priority_rank as value_field,
        count(*) as n_records

    from "quality_measures"."main"."source_priority"
    group by priority_rank

)

select *
from all_values
where value_field not in (
    '1','2','3','4'
)


