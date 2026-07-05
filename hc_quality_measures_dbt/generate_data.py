import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Setup & Reproducibility
np.random.seed(42)
random.seed(42)

NUM_PATIENTS = 200
END_DATE = datetime(2026, 7, 1)
START_DATE = END_DATE - timedelta(days=365)

def random_date(days_back=365):
    return (END_DATE - timedelta(days=random.randint(0, days_back))).strftime('%Y-%m-%d %H:%M:%S')

# 1. Generate Core Patients
patient_ids = [f"PAT_{str(i).zfill(4)}" for i in range(1, NUM_PATIENTS + 1)]
df_patients = pd.DataFrame({
    'patient_id': patient_ids,
    'birth_date': [random_date(25000)[:10] for _ in patient_ids], # Random birthdates up to ~68 years ago
    'gender': np.random.choice(['M', 'F'], size=NUM_PATIENTS)
})

# Define the Hypertension Cohort (~60% of patients) to use across sources
htn_cohort = set(random.sample(patient_ids, int(NUM_PATIENTS * 0.60)))

# 2. Simplified Configurations for Data Generation
diagnosis_sources = {
    'seed_payer_claims.csv': {'pct': 0.60, 'code_col': 'icd10_code', 'date_col': 'service_date'},
    'source_ehr_conditions.csv': {'pct': 0.55, 'code_col': 'condition_code', 'date_col': 'recorded_date'}
}

vital_sources = {
    'source_ehr_vitals.csv': {'pct': 0.70, 'date_col': 'measurement_date', 'sys': 'systolic', 'dia': 'diastolic'},
    'source_patient_reported_vitals.csv': {'pct': 0.40, 'date_col': 'logged_at', 'sys': 'systolic_bp', 'dia': 'diastolic_bp'}
}

# 3. Generate and Save Diagnosis Files
for filename, config in diagnosis_sources.items():
    sampled_patients = random.sample(list(htn_cohort), int(NUM_PATIENTS * config['pct']))
    pd.DataFrame({
        'patient_id': sampled_patients,
        config['date_col']: [random_date(240)[:10] for _ in sampled_patients],
        config['code_col']: 'I10'
    }).to_csv(filename, index=False)

# 4. Generate and Save Vital Files
for filename, config in vital_sources.items():
    vitals_data = []
    sampled_patients = random.sample(patient_ids, int(NUM_PATIENTS * config['pct']))
    
    for pid in sampled_patients:
        # Generate 1 to 3 readings per sampled patient
        for _ in range(random.randint(1, 3)):
            is_htn = pid in htn_cohort
            vitals_data.append({
                'patient_id': pid,
                config['date_col']: random_date(365),
                config['sys']: random.randint(130, 160) if is_htn else random.randint(110, 135),
                config['dia']: random.randint(80, 100) if is_htn else random.randint(70, 85)
            })
            
    pd.DataFrame(vitals_data).to_csv(filename, index=False)

# Save Master Patient List
df_patients.to_csv('seed_patients.csv', index=False)
print("All simplified mock healthcare datasets generated successfully!")
