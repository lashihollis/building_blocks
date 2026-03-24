import duckdb
import pandas as pd
import os

def create_and_load_duckdb():
    """Create DuckDB tables and load CSV data"""
    
    # Connect to database
    conn = duckdb.connect("fhir_data.duckdb")
    
    # Create tables matching your dbt schema
    conn.execute("""
        CREATE OR REPLACE TABLE payer_data (
            patient_id VARCHAR,
            encounter_id VARCHAR,
            encounter_date DATE,
            dx_code VARCHAR,
            vital_type VARCHAR,
            vital_value VARCHAR,
            vital_unit VARCHAR,
            vital_date DATE,
            source_system VARCHAR
        )
    """)
    
    # Load patients
    conn.execute("""
        INSERT INTO payer_data 
        SELECT 
            id as patient_id,
            id as encounter_id,  -- Placeholder
            NULL as encounter_date,
            NULL as dx_code,
            NULL as vital_type,
            NULL as vital_value,
            NULL as vital_unit,
            NULL as vital_date,
            'hapi_fhir' as source_system
        FROM read_csv_auto('data/processed/patients.csv')
    """)
    
    # Load observations as vitals
    conn.execute("""
        CREATE OR REPLACE TABLE vital_data AS
        SELECT 
            patient_id,
            patient_id as encounter_id,  -- Placeholder
            date as vital_date,
            CASE 
                WHEN loinc_code = '8480-6' THEN 'BP_SYSTOLIC'
                WHEN loinc_code = '8462-4' THEN 'BP_DIASTOLIC'
                ELSE loinc_code
            END as vital_type,
            value as vital_value,
            unit as vital_unit,
            'hapi_fhir' as source_system
        FROM read_csv_auto('data/processed/observations.csv')
    """)
    
    print("✅ Data loaded to DuckDB")
    
    # Show sample
    print("\nSample patients:")
    print(conn.execute("SELECT * FROM payer_data LIMIT 3").fetchdf())
    
    print("\nSample vitals:")
    print(conn.execute("SELECT * FROM vital_data LIMIT 5").fetchdf())
    
    return conn

def integrate_with_dbt(dbt_project_path="../analytics_engineering_project"):
    """Copy data to your dbt project's DuckDB and update instructions."""
    import shutil
    
    if os.path.exists(dbt_project_path):
        target_duckdb = os.path.join(dbt_project_path, "fhir_data.duckdb")
        shutil.copy("fhir_data.duckdb", target_duckdb)
        print(f"✅ Copied to {target_duckdb}")
        print("\nNow set your dbt profile to use this file and run:")
        print("cd ../analytics_engineering_project")
        print("dbt run")
        print("dbt test")
    else:
        print("⚠️ dbt project not found at expected path")

if __name__ == "__main__":
    conn = create_and_load_duckdb()
    integrate_with_dbt()
