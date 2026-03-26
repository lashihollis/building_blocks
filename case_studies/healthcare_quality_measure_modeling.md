# Healthcare Quality Measures Data Modeling  
*(analytics_engineering_dbt_project)*

---

## Purpose

Healthcare quality reporting is critical for value-based care, but data comes from multiple sources with varying levels of trust.  

This project builds a scalable **dbt** pipeline that models lab and vital data from three sources—payer, EHR, and patient-reported—to answer a key business question:

> **What percentage of hypertension patients had a blood pressure reading in the last 180 days?**

---

## What This Project Demonstrates

- Multi-source healthcare data integration  
- Source prioritization and ranking logic  
- Layered dbt modeling (**staging → intermediate → marts**)  
- Local development using **DuckDB**

---

## Project Summary

This personal dbt project:

- Simulates three data sources:
  - **Payer** (high trust)  
  - **EHR** (medium trust)  
  - **Patient-reported** (low trust)  

- Applies source ranking using `ROW_NUMBER()` to select the most trusted measurement  

- Calculates quality measures by:
  - Identifying hypertension patients via ICD-10 codes  
  - Finding their most recent blood pressure reading  
  - Flagging compliance within 180 days  

- Generates documentation:
  - Automatic data lineage  
  - Column-level descriptions  

- Produces a final **mart table** that answers the business question with a compliance percentage  

---

## Issues Encountered & Solutions

### Issue 1: DuckDB Date Interval Type Casting

- **Problem:** DuckDB threw an error when subtracting an interval from a string literal  
- **Solution:** Cast the string to a date first  
- **Lesson:** DuckDB requires explicit type casting for date operations  

---

### Issue 2: Source Ranking Across Different Schemas

- **Problem:** Each source had different column names and formats  
  - Example: `bp_systolic` vs `vital_value`  
- **Solution:** Standardized all staging models to use identical column names before unioning  
- **Lesson:** Consistent column naming is essential for clean union logic  

---

### Issue 3: dbt Expectations Package Installation

- **Problem:** `dbt build` failed because `dbt_expectations` was not installed  
- **Solution:**  
  - Created `packages.yml`  
  - Ran `dbt deps`  
- **Lesson:** Always verify package dependencies before running builds  

---

### Issue 4: Seed Data Date Ranges

- **Problem:** Synthetic data used outdated dates (2023–2024), causing "last 180 days" logic to return zero results  
- **Solution:** Updated seed data to recent ranges (March 2025 – March 2026)  
- **Lesson:** Test data must reflect realistic time ranges for accurate validation  

---

## Key Learnings

| Concept              | Takeaway                                                                 |
|---------------------|-------------------------------------------------------------------------|
| **Source Ranking**  | `ROW_NUMBER()` with `CASE` statements effectively implements trust rules |
| **Architecture**    | Layered design improves reusability and clarity                          |
| **DuckDB Quirks**   | Requires explicit date casting; uses `ATTACH` for cross-database queries |
| **Testing**         | dbt tests catch issues early—validate after each layer                   |
| **Documentation**   | `dbt docs serve` provides instant data lineage visibility                |

---

## Final Output

A clean, production-ready **mart table** that calculates:

> ✅ Percentage of hypertension patients with a blood pressure reading in the last 180 days
