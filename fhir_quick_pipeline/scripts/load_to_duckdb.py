import duckdb
import os

def load_to_duckdb(db_path="fhir_data.duckdb"):
    """Load processed CSVs to DuckDB"""
    
    print(f"\n{'='*100}")
    print("Loading data to DuckDB")
    print(f"{'='*100}\n")
    
    conn = duckdb.connect(db_path)
    
    # Load patients
    if os.path.exists("data/processed/patients.csv"):
        conn.execute("""
            CREATE OR REPLACE TABLE patients AS
            SELECT * FROM read_csv_auto('data/processed/patients.csv')
        """)
        patient_count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        print(f"✅ Loaded {patient_count} patients")
    else:
        print("⚠️ patients.csv not found")
    
    # Load observations
    if os.path.exists("data/processed/observations.csv"):
        conn.execute("""
            CREATE OR REPLACE TABLE vitals AS
            SELECT * FROM read_csv_auto('data/processed/observations.csv')
        """)
        vital_count = conn.execute("SELECT COUNT(*) FROM vitals").fetchone()[0]
        print(f"✅ Loaded {vital_count} blood pressure readings")
    else:
        print("⚠️ observations.csv not found")
    
    # Show summary
    print("\n📊 Data Summary:")
    print(conn.execute("SELECT COUNT(*) as total_patients FROM patients").fetchdf())
    print(conn.execute("SELECT vital_type, COUNT(*) as count FROM vitals GROUP BY vital_type").fetchdf())
    
    print("\n📋 Sample Vitals Data:")
    print(conn.execute("SELECT * FROM vitals LIMIT 5").fetchdf())
    
    conn.close()
    print(f"\n✅ Database saved to {db_path}")
    
    return db_path

if __name__ == "__main__":
    load_to_duckdb()
