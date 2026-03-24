import requests
import json
import os
import time

def fetch_patients(base_url="https://hapi.fhir.org/baseR4", max_patients=100):
    """Fetch patients from FHIR server"""
    patients = []
    url = f"{base_url}/Patient"
    params = {"_count": min(max_patients, 20), "_offset": 0}
    
    while len(patients) < max_patients:
        print(f"Fetching patients from {url}")
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        data = response.json()
        
        # Extract patients from FHIR bundle
        for entry in data.get("entry", []):
            patient = entry.get("resource", {})
            name = patient.get("name", [{}])[0]
            patients.append({
                "patient_id": patient.get("id"),
                "gender": patient.get("gender"),
                "birth_date": patient.get("birthDate"),
                "family_name": name.get("family", ""),
                "given_name": " ".join(name.get("given", []))
            })
        
        # Pagination
        next_link = None
        for link in data.get("link", []):
            if link.get("relation") == "next":
                next_link = link.get("url")
                break
        
        if not next_link or len(patients) >= max_patients:
            break
            
        url = next_link
        params = {}
        time.sleep(0.5)
    
    return patients[:max_patients]

def fetch_observations_for_patient(patient_id, base_url="https://hapi.fhir.org/baseR4"):
    """Fetch blood pressure observations for a specific patient"""
    observations = []
    url = f"{base_url}/Observation"
    
    # LOINC codes: 8480-6 = Systolic, 8462-4 = Diastolic
    params = {
        "subject": f"Patient/{patient_id}",
        "code": "http://loinc.org|8480-6,http://loinc.org|8462-4",
        "_count": "20"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return observations
        
        data = response.json()
        
        for entry in data.get("entry", []):
            obs = entry.get("resource", {})
            value = obs.get("valueQuantity", {})
            
            observations.append({
                "patient_id": patient_id,
                "observation_id": obs.get("id"),
                "loinc_code": obs.get("code", {}).get("coding", [{}])[0].get("code"),
                "loinc_display": obs.get("code", {}).get("coding", [{}])[0].get("display"),
                "value": value.get("value"),
                "unit": value.get("unit"),
                "date": obs.get("effectiveDateTime", ""),
                "status": obs.get("status")
            })
    except Exception as e:
        print(f"Error fetching observations for {patient_id}: {e}")
    
    time.sleep(0.3)
    return observations

def save_to_json(data, filename):
    """Save data to JSON file"""
    os.makedirs("data/raw", exist_ok=True)
    with open(f"data/raw/{filename}", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved to data/raw/{filename}")

def fetch_all_data(max_patients=15):
    """Main function to fetch all data"""
    print(f"\n{'='*50}")
    print("Starting FHIR Data Fetch")
    print(f"{'='*50}\n")
    
    print(f"Fetching {max_patients} patients...")
    patients = fetch_patients(max_patients=max_patients)
    print(f"✅ Fetched {len(patients)} patients")
    
    save_to_json(patients, "patients.json")
    
    all_observations = []
    for i, patient in enumerate(patients):
        print(f"Fetching observations for patient {i+1}/{len(patients)}: {patient['patient_id']}")
        obs = fetch_observations_for_patient(patient['patient_id'])
        all_observations.extend(obs)
    
    print(f"\n✅ Fetched {len(all_observations)} total observations")
    save_to_json(all_observations, "observations.json")
    
    return patients, all_observations

if __name__ == "__main__":
    fetch_all_data()
