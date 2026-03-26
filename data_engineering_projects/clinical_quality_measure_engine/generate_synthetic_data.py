"""
Synthetic Healthcare Data Generator (IMPROVED VERSION)
- Dynamic date range (2023 → current year)
- Better performance + realism
- Cleaner structure
"""

import duckdb
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid

# ============================================================
# CONFIG
# ============================================================

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

START_YEAR = 2023
END_YEAR = datetime.now().year  # ✅ always current year

DB_NAME = "quality_measures.duckdb"


# ============================================================
# HELPERS
# ============================================================

def rand_date(year):
    """Generate a random date within a year"""
    return datetime(year, random.randint(1, 12), random.randint(1, 28))


def uid(prefix):
    """Collision-safe IDs"""
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


# ============================================================
# PATIENTS
# ============================================================

def generate_patients(n):
    ages = np.random.choice(
        range(0, 100),
        size=n,
        p=np.array(
            [0.005]*10 + [0.01]*10 + [0.02]*20 + [0.03]*20 +
            [0.025]*20 + [0.01]*20
        )[:100] / sum(
            [0.005]*10 + [0.01]*10 + [0.02]*20 + [0.03]*20 +
            [0.025]*20 + [0.01]*20
        )
    )

    birth_years = END_YEAR - ages

    df = pd.DataFrame({
        "Id": [uid("pat") for _ in range(n)],
        "FIRST": [fake.first_name() for _ in range(n)],
        "LAST": [fake.last_name() for _ in range(n)],
        "BIRTHDATE": [
            f"{y}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            for y in birth_years
        ],
        "GENDER": np.random.choice(["M", "F"], n),
        "RACE": np.random.choice(
            ["white", "black", "asian", "hispanic", "other"], n
        ),
        "STATE": np.random.choice(
            ["CA","TX","NY","FL","IL","PA","OH","GA","NC","MI"], n
        ),
        "INSURANCE": np.random.choice(
            ["Medicare","Medicaid","Commercial","Self-pay"], n
        ),
        "ACTIVE": np.random.choice([True, False], n, p=[0.8, 0.2])
    })

    return df


# ============================================================
# CONDITIONS
# ============================================================

CONDITIONS = [
    ("E11.9", "diabetes", 0.12, True),
    ("I10", "hypertension", 0.25, True),
    ("E78.5", "hyperlipidemia", 0.20, True),
    ("U07.1", "covid", 0.15, False),
    ("F41.9", "anxiety", 0.18, False),
]

def generate_conditions(patients):
    rows = []

    for pid in patients["Id"]:
        for code, desc, prob, chronic in CONDITIONS:
            if random.random() < prob:
                start = rand_date(random.randint(START_YEAR, END_YEAR))

                stop = None
                if not chronic and random.random() < 0.6:
                    stop = start + timedelta(days=random.randint(30, 300))

                rows.append({
                    "Id": uid("cond"),
                    "PATIENT": pid,
                    "CODE": code,
                    "DESCRIPTION": desc,
                    "START": start.date(),
                    "STOP": stop.date() if stop else None
                })

    return pd.DataFrame(rows)


# ============================================================
# OBSERVATIONS (BP)
# ============================================================

def generate_observations(patients, conditions):
    cond_map = conditions.groupby("PATIENT")["DESCRIPTION"].apply(set).to_dict()

    rows = []

    for pid in patients["Id"]:
        conds = cond_map.get(pid, set())

        chronic = "diabetes" in conds or "hypertension" in conds

        for year in range(START_YEAR, END_YEAR + 1):
            n = random.randint(3, 8) if chronic else random.randint(1, 3)

            for _ in range(n):
                date = rand_date(year)

                if chronic:
                    sys = random.randint(120, 160)
                    dia = random.randint(70, 100)
                else:
                    sys = random.randint(105, 130)
                    dia = random.randint(65, 85)

                rows.append({
                    "Id": uid("obs"),
                    "PATIENT": pid,
                    "DATE": date.date(),
                    "VALUE": f"{sys}/{dia}",
                    "TYPE": "blood_pressure"
                })

    return pd.DataFrame(rows)


# ============================================================
# ENCOUNTERS
# ============================================================

def generate_encounters(patients):
    rows = []

    for _, p in patients.iterrows():
        multiplier = 1.5 if p["ACTIVE"] else 0.5
        n = int(random.randint(3, 10) * multiplier)

        for _ in range(n):
            d = rand_date(random.randint(START_YEAR, END_YEAR))

            rows.append({
                "Id": uid("enc"),
                "PATIENT": p["Id"],
                "DATE": d.date(),
                "TYPE": random.choice([
                    "office", "telehealth", "ER", "urgent"
                ])
            })

    return pd.DataFrame(rows)


# ============================================================
# MAIN
# ============================================================

def generate_synthetic_data(n_patients=5000):

    print(f"Generating {n_patients} patients ({START_YEAR}-{END_YEAR})")

    conn = duckdb.connect(DB_NAME)

    patients = generate_patients(n_patients)
    conditions = generate_conditions(patients)
    observations = generate_observations(patients, conditions)
    encounters = generate_encounters(patients)

    conn.execute("CREATE OR REPLACE TABLE patients AS SELECT * FROM patients")
    conn.execute("CREATE OR REPLACE TABLE conditions AS SELECT * FROM conditions")
    conn.execute("CREATE OR REPLACE TABLE observations AS SELECT * FROM observations")
    conn.execute("CREATE OR REPLACE TABLE encounters AS SELECT * FROM encounters")

    print("Done.")
    return conn


if __name__ == "__main__":
    generate_synthetic_data(5000)