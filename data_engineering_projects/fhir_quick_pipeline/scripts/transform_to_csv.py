import pandas as pd
import json
import os

def transform_patients_to_csv():
    """Convert patients JSON to CSV"""
    with open("data/raw/patients.json", "r") as f:
        patients = json.load(f)
    
    df = pd.DataFrame(patients)
    df['source_system'] = 'hapi_fhir'
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/patients.csv", index=False)
    print(f"✅ Saved {len(df)} patients to CSV")

def transform_observations_to_csv():
    """Convert observations JSON to CSV and filter for BP"""
    with open("data/raw/observations.json", "r") as f:
        observations = json.load(f)
    
    df = pd.DataFrame(observations)
    
    # Filter for systolic/diastolic
    bp_codes = ['8480-6', '8462-4', '85354-9']  # Systolic, Diastolic, BP panel
    df = df[df['loinc_code'].isin(bp_codes)]
    
    # Add source tracking
    df['source_system'] = 'hapi_fhir'
    
    # Clean up
    df = df.dropna(subset=['value'])
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/observations.csv", index=False)
    print(f"✅ Saved {len(df)} BP observations to CSV")

if __name__ == "__main__":
    transform_patients_to_csv()
    transform_observations_to_csv()
