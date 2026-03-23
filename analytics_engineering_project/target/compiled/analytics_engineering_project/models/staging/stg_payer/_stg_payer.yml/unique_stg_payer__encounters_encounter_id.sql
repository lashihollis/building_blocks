
    
    

select
    encounter_id as unique_field,
    count(*) as n_records

from "analytics_engineering_project"."main"."stg_payer__encounters"
where encounter_id is not null
group by encounter_id
having count(*) > 1


