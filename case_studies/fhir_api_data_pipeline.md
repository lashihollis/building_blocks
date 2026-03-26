# FHIR API Data Pipeline
*(data_engineering_projects/fhir_quick_pipeline)*
---

## Purpose

Healthcare interoperability is a major challenge—different systems (Epic, Cerner, Athena) store data in inconsistent formats.  

**FHIR (Fast Healthcare Interoperability Resources)** is the industry standard for exchanging healthcare data, but working with FHIR APIs introduces its own complexities.

This project builds a Python-based data pipeline that:

1. **Ingests real synthetic patient data** from a public FHIR API  
2. **Transforms nested JSON** into analytics-ready CSV files  
3. **Loads data into DuckDB** and integrates with dbt quality models  

---

## What This Project Demonstrates

- API ingestion and error handling  
- JSON → relational data transformation  
- Multi-database integration using DuckDB  
- End-to-end data pipeline orchestration  

---

## Project Summary

This pipeline performs the following steps:

1. **Fetches 100 patients**  
   - Source: HAPI FHIR server (free synthetic dataset)
2. **Extracts blood pressure observations**  
   - Uses LOINC codes:
     - `8480-6` → Systolic  
     - `8462-4` → Diastolic  
3. **Transforms FHIR JSON → CSV**  
   - Flattens nested structures  
   - Uses Python’s built-in `csv` module (no pandas dependency)
4. **Loads into DuckDB**  
   - Attaches to an existing dbt project  
5. **Generates quality measures**  
   - Combines FHIR data with previously modeled synthetic datasets  

---

## Key Outcome

A reusable, extensible pipeline that can:

> ✅ Ingest FHIR data from any compliant API  
> ✅ Transform complex healthcare JSON into analytics-ready tables  
> ✅ Integrate seamlessly with downstream dbt models  

---

## Issues Encountered & Solutions

### Issue 1: DuckDB Cross-Database Queries

- **Problem:** Unable to reference FHIR tables within dbt  
- **Root Cause:** dbt was connected to only one DuckDB file; the FHIR database was not attached  
- **Solution:** Used DuckDB’s `ATTACH` command to connect multiple databases  

---

### Issue 2: FHIR Data Structure Variation

- **Problem:**  
  The FHIR vitals table used `vital_type` (e.g., `BP_SYSTOLIC`) instead of `loinc_code` (e.g., `8480-6`)
- **Root Cause:**  
  The transformation script had already mapped LOINC codes to human-readable vital types, while dbt checks expected raw LOINC codes  
- **Solution:**  
  Updated validation logic to accept either:
  - `loinc_code`  
  - `vital_type`  
- **Lesson:**  
  Data pipelines must handle schema variability—flexible validation logic is critical  

---

## Key Learnings

| Concept                     | Takeaway                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| **FHIR APIs**              | Powerful but complex due to deeply nested JSON structures               |
| **Data Transformation**    | Flattening JSON is essential for analytics use cases                    |
| **DuckDB Integration**     | `ATTACH` enables multi-database workflows                               |
| **Schema Flexibility**     | Pipelines must adapt to multiple representations of the same data       |
| **Pipeline Design**        | Lightweight Python (no pandas) can still power robust data pipelines    |
