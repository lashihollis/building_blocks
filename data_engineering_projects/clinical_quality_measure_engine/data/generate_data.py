"""Generate comprehensive synthetic clinical data for multiple quality measures."""
import duckdb
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for realistic data generation
fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)

def generate_patients(n=1000):
    """Generate synthetic patient records with multiple conditions."""
    patients = []
    
    for i in range(n):
        patient_id = f'P{i+1:04d}'
        age = random.randint(18, 95)
        
        # Generate multiple clinical conditions (realistic prevalence)
        # These probabilities are based on typical population rates
        patients.append({
            'patient_id': patient_id,
            'age': age,
            'gender': random.choice(['M', 'F']),
            'race': random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Other']),
            
            # Clinical conditions
            'has_diabetes': random.random() < 0.25,      # 25% diabetes prevalence
            'has_hypertension': random.random() < 0.35,  # 35% hypertension prevalence
            'has_heart_failure': random.random() < 0.10, # 10% heart failure prevalence
            'has_copd': random.random() < 0.08,          # 8% COPD prevalence
            'has_depression': random.random() < 0.15,    # 15% depression prevalence
            
            # Pregnancy flag (for exclusions)
            'is_pregnant': random.random() < 0.05 if random.choice(['F']) == 'F' else False,
            
            # Hospice care (for exclusions)
            'hospice_care': random.random() < 0.02 if age > 75 else False,
            
            # Smoking status (for certain measures)
            'smoking_status': random.choices(['never', 'former', 'current'], 
                                            weights=[0.6, 0.25, 0.15], 
                                            k=1)[0],
            
            # BMI
            'bmi': round(random.uniform(18.5, 45.0), 1)
        })
    
    print(f"Generated {len(patients)} patients")
    print(f"  - Diabetes: {sum(1 for p in patients if p['has_diabetes'])} ({sum(1 for p in patients if p['has_diabetes'])/len(patients)*100:.1f}%)")
    print(f"  - Hypertension: {sum(1 for p in patients if p['has_hypertension'])} ({sum(1 for p in patients if p['has_hypertension'])/len(patients)*100:.1f}%)")
    print(f"  - Heart Failure: {sum(1 for p in patients if p['has_heart_failure'])} ({sum(1 for p in patients if p['has_heart_failure'])/len(patients)*100:.1f}%)")
    
    return pd.DataFrame(patients)

def generate_encounters(patients_df):
    """Generate encounter records for all patients."""
    encounters = []
    
    for _, patient in patients_df.iterrows():
        # Number of encounters varies by patient health status
        n_encounters = random.randint(1, 15)
        
        for _ in range(n_encounters):
            encounter_date = fake.date_between(start_date='-2y', end_date='today')
            encounters.append({
                'patient_id': patient['patient_id'],
                'encounter_id': fake.uuid4(),
                'encounter_date': encounter_date,
                'encounter_type': random.choice(['outpatient', 'inpatient', 'emergency', 'wellness']),
                'provider_id': f'PROV{random.randint(1, 50):03d}'
            })
    
    return pd.DataFrame(encounters)

def generate_blood_pressure_readings(patients_df, encounters_df):
    """Generate blood pressure readings with realistic control rates by condition."""
    bp_readings = []
    
    # Only generate BP readings for patients with relevant conditions
    relevant_patients = patients_df[
        patients_df['has_diabetes'] | 
        patients_df['has_hypertension'] | 
        patients_df['has_heart_failure']
    ]
    
    # Get encounters for relevant patients
    relevant_encounters = encounters_df[encounters_df['patient_id'].isin(relevant_patients['patient_id'])]
    
    for _, encounter in relevant_encounters.iterrows():
        # Get patient data
        patient = patients_df[patients_df['patient_id'] == encounter['patient_id']].iloc[0]
        
        # Control rate depends on conditions and care quality
        # Different conditions have different target rates
        if patient['has_hypertension']:
            # Hypertension patients: ~65% controlled
            is_controlled = random.random() < 0.65
        elif patient['has_diabetes']:
            # Diabetes patients: ~70% controlled
            is_controlled = random.random() < 0.70
        else:
            # General population: ~75% controlled
            is_controlled = random.random() < 0.75
        
        if is_controlled:
            systolic = random.randint(110, 129)
            diastolic = random.randint(70, 79)
        else:
            systolic = random.randint(130, 180)
            diastolic = random.randint(80, 100)
        
        bp_readings.append({
            'patient_id': encounter['patient_id'],
            'encounter_id': encounter['encounter_id'],
            'encounter_date': encounter['encounter_date'],
            'systolic_bp': systolic,
            'diastolic_bp': diastolic,
            'bp_date': encounter['encounter_date']
        })
    
    return pd.DataFrame(bp_readings)

def generate_lab_results(patients_df, encounters_df):
    """Generate lab results for various clinical measures."""
    labs = []
    
    # Common lab tests for quality measures
    lab_tests = [
        {'name': 'hba1c', 'unit': '%', 'diabetes_related': True},
        {'name': 'ldl', 'unit': 'mg/dL', 'diabetes_related': True},
        {'name': 'creatinine', 'unit': 'mg/dL', 'general': True},
        {'name': 'bun', 'unit': 'mg/dL', 'general': True}
    ]
    
    # Generate labs for patients with relevant conditions
    for _, patient in patients_df.iterrows():
        # Get encounters for this patient
        patient_encounters = encounters_df[encounters_df['patient_id'] == patient['patient_id']]
        
        for _, encounter in patient_encounters.iterrows():
            # Generate HbA1c for diabetic patients
            if patient['has_diabetes'] and random.random() < 0.3:  # 30% of encounters have HbA1c
                if random.random() < 0.65:  # 65% controlled
                    hba1c = round(random.uniform(5.5, 7.0), 1)
                else:
                    hba1c = round(random.uniform(7.1, 10.0), 1)
                
                labs.append({
                    'patient_id': patient['patient_id'],
                    'encounter_id': encounter['encounter_id'],
                    'lab_date': encounter['encounter_date'],
                    'lab_name': 'hba1c',
                    'lab_value': hba1c,
                    'lab_unit': '%'
                })
            
            # Generate LDL for diabetic/hypertensive patients
            if (patient['has_diabetes'] or patient['has_hypertension']) and random.random() < 0.25:
                if random.random() < 0.60:  # 60% controlled (<100 mg/dL)
                    ldl = random.randint(60, 99)
                else:
                    ldl = random.randint(100, 190)
                
                labs.append({
                    'patient_id': patient['patient_id'],
                    'encounter_id': encounter['encounter_id'],
                    'lab_date': encounter['encounter_date'],
                    'lab_name': 'ldl',
                    'lab_value': ldl,
                    'lab_unit': 'mg/dL'
                })
    
    return pd.DataFrame(labs)

def generate_medications(patients_df):
    """Generate medication prescriptions."""
    meds = []
    
    medications = {
        'diabetes': ['metformin', 'insulin', 'glipizide', 'sitagliptin'],
        'hypertension': ['lisinopril', 'amlodipine', 'losartan', 'metoprolol'],
        'heart_failure': ['furosemide', 'carvedilol', 'spironolactone', 'digoxin']
    }
    
    for _, patient in patients_df.iterrows():
        # Diabetes medications
        if patient['has_diabetes'] and random.random() < 0.8:  # 80% on medication
            med_count = random.randint(1, 2)
            for _ in range(med_count):
                meds.append({
                    'patient_id': patient['patient_id'],
                    'medication_name': random.choice(medications['diabetes']),
                    'prescription_date': fake.date_between(start_date='-1y', end_date='today'),
                    'active': random.random() < 0.9  # 90% still active
                })
        
        # Hypertension medications
        if patient['has_hypertension'] and random.random() < 0.75:
            med_count = random.randint(1, 2)
            for _ in range(med_count):
                meds.append({
                    'patient_id': patient['patient_id'],
                    'medication_name': random.choice(medications['hypertension']),
                    'prescription_date': fake.date_between(start_date='-1y', end_date='today'),
                    'active': random.random() < 0.85
                })
    
    return pd.DataFrame(meds)

def generate_data(db_path='clinical_data.duckdb'):
    """Generate all synthetic data and load into DuckDB."""
    
    print("\n" + "="*60)
    print("SYNTHETIC CLINICAL DATA GENERATION")
    print("="*60)
    
    # Generate all datasets
    print("\n📊 Generating patient data...")
    patients = generate_patients(1000)
    
    print("\n🏥 Generating encounter data...")
    encounters = generate_encounters(patients)
    print(f"  Generated {len(encounters)} encounters")
    
    print("\n❤️ Generating blood pressure readings...")
    bp_readings = generate_blood_pressure_readings(patients, encounters)
    print(f"  Generated {len(bp_readings)} BP readings")
    
    print("\n🔬 Generating lab results...")
    labs = generate_lab_results(patients, encounters)
    print(f"  Generated {len(labs)} lab results")
    
    print("\n💊 Generating medications...")
    medications = generate_medications(patients)
    print(f"  Generated {len(medications)} prescriptions")
    
    # Connect to DuckDB
    print(f"\n💾 Loading data into DuckDB: {db_path}")
    conn = duckdb.connect(db_path)
    
    # Create tables and load data
    conn.execute("CREATE OR REPLACE TABLE patients AS SELECT * FROM patients")
    conn.execute("CREATE OR REPLACE TABLE encounters AS SELECT * FROM encounters")
    conn.execute("CREATE OR REPLACE TABLE blood_pressure AS SELECT * FROM bp_readings")
    conn.execute("CREATE OR REPLACE TABLE lab_results AS SELECT * FROM labs")
    conn.execute("CREATE OR REPLACE TABLE medications AS SELECT * FROM medications")
    
    # Verify data
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    print(f"Database: {db_path}")
    print(f"\nTable counts:")
    print(f"  patients:        {conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0]:,}")
    print(f"  encounters:      {conn.execute('SELECT COUNT(*) FROM encounters').fetchone()[0]:,}")
    print(f"  blood_pressure:  {conn.execute('SELECT COUNT(*) FROM blood_pressure').fetchone()[0]:,}")
    print(f"  lab_results:     {conn.execute('SELECT COUNT(*) FROM lab_results').fetchone()[0]:,}")
    print(f"  medications:     {conn.execute('SELECT COUNT(*) FROM medications').fetchone()[0]:,}")
    
    conn.close()
    print("\n✓ Data generation complete!")

if __name__ == "__main__":
    generate_data()
