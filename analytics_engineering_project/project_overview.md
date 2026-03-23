Healthcare Quality Measures Data Modeling

Project Overview
This project demonstrates a scalable approach to modeling healthcare lab and vital data for quality measure reporting. Using dbt and DuckDB, I simulate data from three sources (payer, EHR, patient-reported), apply source ranking based on trustworthiness, and answer a real business question:

What percentage of patients with a hypertension diagnosis have had a blood pressure reading within the last six months (based on synthetic data date ranges)?

This project showcases:
    1.Multi-source data integration
    2.Source prioritization and ranking logic
    3.Layered dbt modeling (staging → intermediate → marts)
    4.Quality measure calculation
    5.Local development with DuckDB

Business Context
In value-based care, quality measures track whether patients receive recommended care. A common measure for hypertension is: "Did patients with hypertension have their blood pressure checked in the past six months (based on synthetic data date ranges)?"

Answering this requires:
    1.Identifying patients with a hypertension diagnosis
    2.Finding their most recent blood pressure reading
    3.Determining if that reading occurred within the last 180 days

Data often comes from multiple sources with varying levels of trust:
    1.Payer data — claims-based, structured, high trust
    2.EHR data — clinical, reliable but may have gaps
    3.Patient-reported — convenient but lowest trust
