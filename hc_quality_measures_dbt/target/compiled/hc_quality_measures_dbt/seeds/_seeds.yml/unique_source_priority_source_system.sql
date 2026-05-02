
    
    

select
    source_system as unique_field,
    count(*) as n_records

from "quality_measures"."main"."source_priority"
where source_system is not null
group by source_system
having count(*) > 1


