
    
    

with child as (
    select dx_code as from_field
    from "analytics_engineering_project"."main"."stg_ehr__diagnosis"
    where dx_code is not null
),

parent as (
    select dx_code as to_field
    from "analytics_engineering_project"."main"."dx_codes"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


