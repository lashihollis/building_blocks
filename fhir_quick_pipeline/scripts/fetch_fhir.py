import requests
import json
import os
import time

# Constants for better maintainability
BASE_URL = "https://hapi.fhir.org/baseR4"
DATA_DIR = "fhir_quick_pipeline/data/raw"

###
# HELPER: fetch_patients
# Connects to the FHIR Patient endpoint and handles pagination logic.
# It extracts key demographic details (ID, Gender, Name) from the JSON Bundle
# and returns a list of simplified dictionaries.
###
def fetch_patients(max_patients=50):
    patients = []
    url = f"{BASE_URL}/Patient"
    params = {"_count": min(max_patients, 100)}
    
    with requests.Session() as session:
        while len(patients) < max_patients:
            try:
                response = session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                for entry in data.get("entry", []):
                    resource = entry.get("resource", {})
                    # Simplify name extraction
                    names = resource.get("name", [{}])
                    primary_name = names[0] if names else {}
                    
                    patients.append({
                        "patient_id": resource.get("id"),
                        "gender": resource.get("gender"),
                        "birth_date": resource.get("birthDate"),
                        "family_name": primary_name.get("family", ""),
                        "given_name": " ".join(primary_name.get("given", []))
                    })
                    
                    if len(patients) >= max_patients:
                        break
                
                # Check for next page in FHIR Bundle links
                next_link = next((link["url"] for link in data.get("link", []) if link["relation"] == "next"), None)
                
                if not next_link or len(patients) >= max_patients:
                    break
                    
                url = next_link
                params = {}  # Clear params as they are usually baked into the next_link URL
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching patients: {e}")
                break
                
    return patients

###
# HELPER: fetch_observations_for_patient
# Targets specific LOINC codes (Systolic/Diastolic BP) for a single patient.
# It filters for 'subject' ID and returns observation values with their units.
###
def fetch_observations_for_patient(session, patient_id):
    observations = []
    url = f"{BASE_URL}/Observation"
    
    # LOINC codes: 8480-6 = Systolic, 8462-4 = Diastolic
    params = {
        "subject": f"Patient/{patient_id}",
        "code": "http://loinc.org|8480-6,http://loinc.org|8462-4",
        "_count": "20"
    }
    
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for entry in data.get("entry", []):
            obs = entry.get("resource", {})
            val_qty = obs.get("valueQuantity", {})
            coding = obs.get("code", {}).get("coding", [{}])[0]
            
            observations.append({
                "patient_id": patient_id,
                "observation_id": obs.get("id"),
                "loinc_code": coding.get("code"),
                "loinc_display": coding.get("display"),
                "value": val_qty.get("value"),
                "unit": val_qty.get("unit"),
                "date": obs.get("effectiveDateTime", ""),
                "status": obs.get("status")
            })
    except Exception as e:
        print(f"⚠️ Could not fetch observations for {patient_id}: {e}")
    
    return observations

###
# HELPER: save_to_json
# A utility function to ensure the directory exists and write the list
# of data objects to a formatted JSON file.
###
def save_to_json(data, filename):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Data successfully saved to {filepath}")

###
# MAIN: fetch_all_data
# The orchestrator function. It first pulls the patient list, then loops
# through each patient to grab their specific clinical observations.
###
def fetch_all_data(max_patients=100):
    print(f"\n{'='*40}")
    print("🚀 INITIATING FHIR PIPELINE")
    print(f"\n{'='*40}\n")
    
    # Get Patients
    patients = fetch_patients(max_patients=max_patients)
    print(f"✅ Extracted {len(patients)} patients.")
    save_to_json(patients, "patients.json")
    
    # Get Observations using a shared Session
    all_observations = []
    with requests.Session() as session:
        for i, pt in enumerate(patients, 1):
            pid = pt['patient_id']
            if not pid: continue
            
            print(f"🔄 [{i}/{len(patients)}] Fetching vitals for: {pid}")
            obs_list = fetch_observations_for_patient(session, pid)
            all_observations.extend(obs_list)
            time.sleep(0.2) # Polite rate limiting
    
    print(f"\n✅ Total Observations Collected: {len(all_observations)}")
    save_to_json(all_observations, "observations.json")
    
    return patients, all_observations

if __name__ == "__main__":
    fetch_all_data()