# 🏥 FHIR Data Pipeline Project

## Overview
Build a Python-based data pipeline that ingests real-world healthcare data from a public FHIR API, transforms it, and prepares it for downstream analytics.

## Objectives
This project will:

- Fetch real patient data from a public FHIR API  
- Extract labs and vital signs for use in a dbt data pipeline  
- Save processed data to CSV files  
- Load the data into DuckDB for analysis  

## Tech Stack
- **Python** – data ingestion and processing  
- **FHIR API** – healthcare data source  
- **dbt** – data transformation (downstream) -- hc_quality_measures_dbt
- **DuckDB** – analytics and querying  
- **CSV** – intermediate storage format  

## Future Enhancements
- Add streaming simulation for real-time data ingestion  
- Expand dataset to include additional FHIR resources  
- Build dbt models for analytics-ready tables  
- Create dashboards on top of DuckDB  
