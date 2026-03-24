import json
import csv
import os
from datetime import datetime

def transform_patients_to_csv():
    """Convert patients JSON to CSV"""
    with open("data/raw/patients.json", "r") as f:
        patients = json.load(f)
    
    if not patients:
        print("⚠️ No patients data found")
        return None
    
    os.makedirs("data/processed", exist_ok=True)
    
    ingestion_date = datetime.now().isoformat()
    
    with open("data/processed/patients.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "patient_id", "gender", "birth_date", 
            "family_name", "given_name", "source_system", "ingestion_date"
        ])
        writer.writeheader()
        
        for p in patients:
            writer.writerow({
                "patient_id": p.get("patient_id"),
                "gender": p.get("gender"),
                "birth_date": p.get("birth_date"),
                "family_name": p.get("family_name"),
                "given_name": p.get("given_name"),
                "source_system": "hapi_fhir",
                "ingestion_date": ingestion_date
            })
    
    print(f"✅ Saved {len(patients)} patients to data/processed/patients.csv")
    return patients

def transform_observations_to_csv():
    """Convert observations JSON to CSV"""
    with open("data/raw/observations.json", "r") as f:
        observations = json.load(f)
    
    if not observations:
        print("⚠️ No observations data found")
        return None
    
    # Filter for BP readings (systolic and diastolic)
    bp_observations = []
    for obs in observations:
        loinc = obs.get("loinc_code")
        if loinc in ["8480-6", "8462-4"] and obs.get("value") is not None:
            bp_observations.append(obs)
    
    if not bp_observations:
        print("⚠️ No blood pressure observations found")
        return None
    
    os.makedirs("data/processed", exist_ok=True)
    
    ingestion_date = datetime.now().isoformat()
    vital_type_map = {"8480-6": "BP_SYSTOLIC", "8462-4": "BP_DIASTOLIC"}
    
    with open("data/processed/observations.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "patient_id", "vital_date", "vital_type", 
            "vital_value", "vital_unit", "source_system", "ingestion_date"
        ])
        writer.writeheader()
        
        for obs in bp_observations:
            writer.writerow({
                "patient_id": obs.get("patient_id"),
                "vital_date": obs.get("date", "")[:10] if obs.get("date") else "",
                "vital_type": vital_type_map.get(obs.get("loinc_code")),
                "vital_value": obs.get("value"),
                "vital_unit": obs.get("unit"),
                "source_system": "hapi_fhir",
                "ingestion_date": ingestion_date
            })
    
    print(f"✅ Saved {len(bp_observations)} BP observations to data/processed/observations.csv")
    return bp_observations

if __name__ == "__main__":
    patients = transform_patients_to_csv()
    observations = transform_observations_to_csv()
    
    if patients:
        print(f"\n📊 Summary:")
        print(f"   Patients: {len(patients)}")
        if observations:
            print(f"   BP Readings: {len(observations)}")
