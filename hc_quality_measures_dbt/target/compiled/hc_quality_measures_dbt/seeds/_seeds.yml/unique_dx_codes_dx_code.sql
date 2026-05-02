
    
    

select
    dx_code as unique_field,
    count(*) as n_records

from "quality_measures"."main"."dx_codes"
where dx_code is not null
group by dx_code
having count(*) > 1


