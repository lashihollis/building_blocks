import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# Setup & Reproducibility
np.random.seed(42)
random.seed(42)

NUM_PATIENTS = 200
END_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=365)
PROJECT_DIR = Path(__file__).resolve().parent
SEEDS_DIR = PROJECT_DIR / "seeds"
SEEDS_DIR.mkdir(parents=True, exist_ok=True)


def random_date(days_back=365):
    return (END_DATE - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d %H:%M:%S")


def write_csv(filename, dataframe):
    output_path = SEEDS_DIR / filename
    dataframe.to_csv(output_path, index=False)
    return output_path


def remove_legacy_outputs():
    legacy_files = [
        "seed_patients.csv",
        "seed_payer_claims.csv",
        "source_ehr_conditions.csv",
        "source_ehr_vitals.csv",
        "source_patient_reported_vitals.csv",
    ]
    for base_dir in [PROJECT_DIR, PROJECT_DIR.parent]:
        for filename in legacy_files:
            candidate = base_dir / filename
            if candidate.exists():
                candidate.unlink()


remove_legacy_outputs()

# 1. Generate Core Patients
patient_ids = [f"PAT_{str(i).zfill(4)}" for i in range(1, NUM_PATIENTS + 1)]
df_patients = pd.DataFrame(
    {
        "patient_id": patient_ids,
        "birth_date": [random_date(25000)[:10] for _ in patient_ids],  # Random birthdates up to ~68 years ago
        "gender": np.random.choice(["M", "F"], size=NUM_PATIENTS),
    }
)

# Define the Hypertension Cohort (~60% of patients) to use across sources
htn_cohort = set(random.sample(patient_ids, int(NUM_PATIENTS * 0.60)))

# 2. Generate diagnosis and vitals source files for the dbt seeds folder
payer_rows = []
ehr_rows = []
patient_reported_rows = []

for patient_id in patient_ids:
    encounter_id = f"ENC_{patient_id.split('_')[1]}"
    encounter_date = random_date(180)[:10]
    is_htn = patient_id in htn_cohort

    # Payer diagnosis and vitals rows
    payer_rows.append(
        {
            "patient_id": patient_id,
            "encounter_id": encounter_id,
            "encounter_date": encounter_date,
            "dx_code": "I10",
            "vital_type": None,
            "vital_value": None,
            "vital_unit": None,
            "vital_date": None,
        }
    )

    if random.random() < 0.8:
        vital_date = random_date(180)[:10]
        systolic = random.randint(130, 160) if is_htn else random.randint(110, 135)
        diastolic = random.randint(80, 100) if is_htn else random.randint(70, 85)
        payer_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "encounter_date": encounter_date,
                "dx_code": None,
                "vital_type": "BP_SYSTOLIC",
                "vital_value": systolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )
        payer_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "encounter_date": encounter_date,
                "dx_code": None,
                "vital_type": "BP_DIASTOLIC",
                "vital_value": diastolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )

    # EHR diagnosis and vitals rows
    if random.random() < 0.55:
        ehr_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "encounter_date": encounter_date,
                "dx_code": "I10",
                "vital_type": None,
                "vital_value": None,
                "vital_unit": None,
                "vital_date": None,
            }
        )

    if random.random() < 0.7:
        vital_date = random_date(180)[:10]
        systolic = random.randint(130, 160) if is_htn else random.randint(110, 135)
        diastolic = random.randint(80, 100) if is_htn else random.randint(70, 85)
        ehr_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "encounter_date": encounter_date,
                "dx_code": None,
                "vital_type": "BP_SYSTOLIC",
                "vital_value": systolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )
        ehr_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "encounter_date": encounter_date,
                "dx_code": None,
                "vital_type": "BP_DIASTOLIC",
                "vital_value": diastolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )

    # Patient-reported vitals rows
    if random.random() < 0.4:
        vital_date = random_date(180)[:10]
        systolic = random.randint(130, 160) if is_htn else random.randint(110, 135)
        diastolic = random.randint(80, 100) if is_htn else random.randint(70, 85)
        patient_reported_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": None,
                "encounter_date": encounter_date,
                "vital_type": "BP_SYSTOLIC",
                "vital_value": systolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )
        patient_reported_rows.append(
            {
                "patient_id": patient_id,
                "encounter_id": None,
                "encounter_date": encounter_date,
                "vital_type": "BP_DIASTOLIC",
                "vital_value": diastolic,
                "vital_unit": "mmHg",
                "vital_date": vital_date,
            }
        )

# 3. Generate and save the source files expected by the workflow and dbt seeds
write_csv("seed_patients.csv", df_patients)
write_csv(
    "source_payer_claims.csv",
    pd.DataFrame(
        {
            "patient_id": random.sample(patient_ids, int(NUM_PATIENTS * 0.60)),
            "service_date": [random_date(240)[:10] for _ in range(int(NUM_PATIENTS * 0.60))],
            "icd10_code": "I10",
        }
    ),
)
write_csv(
    "source_ehr_conditions.csv",
    pd.DataFrame(
        {
            "patient_id": random.sample(patient_ids, int(NUM_PATIENTS * 0.55)),
            "recorded_date": [random_date(240)[:10] for _ in range(int(NUM_PATIENTS * 0.55))],
            "condition_code": "I10",
        }
    ),
)
write_csv(
    "source_ehr_vitals.csv",
    pd.DataFrame(
        {
            "patient_id": random.sample(patient_ids, int(NUM_PATIENTS * 0.70)),
            "measurement_date": [random_date(365) for _ in range(int(NUM_PATIENTS * 0.70))],
            "systolic": [random.randint(130, 160) for _ in range(int(NUM_PATIENTS * 0.70))],
            "diastolic": [random.randint(80, 100) for _ in range(int(NUM_PATIENTS * 0.70))],
        }
    ),
)
write_csv(
    "source_patient_reported_vitals.csv",
    pd.DataFrame(
        {
            "patient_id": random.sample(patient_ids, int(NUM_PATIENTS * 0.40)),
            "logged_at": [random_date(365) for _ in range(int(NUM_PATIENTS * 0.40))],
            "systolic_bp": [random.randint(130, 160) for _ in range(int(NUM_PATIENTS * 0.40))],
            "diastolic_bp": [random.randint(80, 100) for _ in range(int(NUM_PATIENTS * 0.40))],
        }
    ),
)

# 4. Save staging-friendly seed files used by the dbt models
write_csv("payer_data.csv", pd.DataFrame(payer_rows))
write_csv("ehr_data.csv", pd.DataFrame(ehr_rows))
write_csv("patient_reported_data.csv", pd.DataFrame(patient_reported_rows))

print("All simplified mock healthcare datasets generated successfully!")
