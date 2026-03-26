# Create the data generator file

"""Generate minimal synthetic data for testing quality measures."""
import duckdb
import pandas as pd
from faker import Faker
import random

# Initialize Faker for generating realistic-looking data
# Set seeds for reproducible results (same data every run)
fake = Faker()
random.seed(42)  # Ensures random numbers are the same each run

def generate_data(db_path='clinical_data.duckdb'):
    """Generate synthetic patient and clinical data.
    
    This creates:
    1. Patient demographics (with diabetes flag)
    2. Blood pressure readings for diabetic patients
    """
    
    print("Generating synthetic patient data...")
    
    # Generate 500 patients
    # Using a list comprehension to create patient records
    patients = []
    for i in range(500):
        patients.append({
            'patient_id': f'P{i+1:04d}',  # Format: P0001, P0002, etc.
            'has_diabetes': random.random() < 0.25,  # 25% have diabetes (realistic prevalence)
            'age': random.randint(18, 90)  # Adult patients aged 18-90
        })
    
    print(f"Generated {len(patients)} patients")
    print(f"  - Diabetic patients: {sum(1 for p in patients if p['has_diabetes'])}")
    
    # Generate blood pressure readings ONLY for diabetic patients
    # This simulates that only diabetic patients get regular BP monitoring
    bp_readings = []
    for patient in patients:
        if patient['has_diabetes']:
            # Simulate blood pressure control rates
            # In a real clinical setting, about 60-70% of diabetic patients have controlled BP
            is_controlled = random.random() < 0.7  # 70% controlled
            
            if is_controlled:
                # Controlled BP: < 140/90
                systolic = random.randint(110, 129)
                diastolic = random.randint(70, 79)
            else:
                # Uncontrolled BP: >= 140/90
                systolic = random.randint(130, 180)
                diastolic = random.randint(80, 100)
            
            bp_readings.append({
                'patient_id': patient['patient_id'],
                'systolic_bp': systolic,
                'diastolic_bp': diastolic,
                'measurement_date': fake.date_between(start_date='-1y', end_date='today')
            })
    
    print(f"Generated {len(bp_readings)} blood pressure readings")
    
    # Convert Python dictionaries to pandas DataFrames
    # DataFrames make it easy to load into DuckDB
    patients_df = pd.DataFrame(patients)
    bp_df = pd.DataFrame(bp_readings)
    
    # Connect to DuckDB (creates file if it doesn't exist)
    print(f"\nConnecting to DuckDB database: {db_path}")
    conn = duckdb.connect(db_path)
    
    # Create tables and load data
    # The REPLACE OR CREATE pattern ensures we start fresh each run
    print("Creating patients table...")
    conn.execute("CREATE OR REPLACE TABLE patients AS SELECT * FROM patients_df")
    
    print("Creating blood_pressure table...")
    conn.execute("CREATE OR REPLACE TABLE blood_pressure AS SELECT * FROM bp_df")
    
    # Verify the data loaded correctly
    patient_count = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    bp_count = conn.execute("SELECT COUNT(*) FROM blood_pressure").fetchone()[0]
    diabetic_count = conn.execute("SELECT COUNT(*) FROM patients WHERE has_diabetes = true").fetchone()[0]
    
    # Close the connection
    conn.close()
    
    # Print summary
    print("\n" + "="*50)
    print("DATA GENERATION COMPLETE")
    print("="*50)
    print(f"Database location: {db_path}")
    print(f"Total patients: {patient_count}")
    print(f"Diabetic patients: {diabetic_count}")
    print(f"Blood pressure readings: {bp_count}")
    print(f"Average BP readings per diabetic: {bp_count/diabetic_count:.1f}")
    print("="*50)
    
    return db_path

# Allow running this file directly for testing
if __name__ == "__main__":
    generate_data()
