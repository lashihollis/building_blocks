prompt:

I want to create a Clinical Quality Measure Engine that will take maybe 3 hours to build.
I want it to be a working quality measure calculator that: Takes a YAML definition for ONE quality measure (e.g., "Diabetic patients with controlled blood pressure" --eventually scale to more) Executes it against synthetically generated data using DuckDB. Outputs a clean report with numerator, denominator, exclusion counts Includes a simple way to add new measures.

how would you suggest i complete this project?

can walk through the project step by step including explanations for your coding choices?

what should the folder structure look like? 
i have a main folder of clinical_quality_measures_engine. what should the structure be under this?

i want to go folder by folder file by file and create the project.
i want to end up with a mvp that could easily be scalable.