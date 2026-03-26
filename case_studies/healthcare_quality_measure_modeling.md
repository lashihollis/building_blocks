Healthcare Quality Measures Data Modeling
(analytics_engineering_dbt_project)
-----------------------------------------

Purpose
-------
Healthcare quality reporting is critical for value-based care, but data comes from multiple sources with varying levels of trust. I built a scalable dbt project that models lab and vital data from three sources (payer, EHR, patient-reported) to answer a key business question: What percentage of hypertension patients had a blood pressure reading in the last 180 days?

This project demonstrates:
    - Multi-source healthcare data integration
    - Source prioritization and ranking logic
    - Layered dbt modeling (staging → intermediate → marts)
    - Local development with DuckDB

Summary
-------

I created a personal dbt project that:

    -Simulates three data sources: payer (high trust), EHR (medium trust), patient-reported (low trust)
    -Applies source ranking that uses ROW_NUMBER() to select the most trusted source for each measurement
    -Calculates quality measures to identify hypertension patients via ICD-10 codes, finds their most recent BP reading, and flags compliance within 180 days
    -Generates documentation — automatic data lineage and column-level descriptions
    -The final output is a clean mart table that answers the business question with a compliance percentage.
