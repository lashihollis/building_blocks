import csv
from pathlib import Path

def create_mock_csv(target_path: Path, num_rows: int = 100):
    """Generates a realistic, raw healthcare encounter CSV for testing."""
    headers = ["encounter_id", "patient_id", "plan_id", "department_id", "billing_amount", "encounter_date"]
    
    # Sample pool to create relational lookups
    base_rows = [
        ["ENC1001", "P900", "PLAN_BLUE", "DEPT_ER", "1250.50", "2026-06-01"],
        ["ENC1002", "P901", "PLAN_GOLD", "DEPT_ICU", "5400.00", "2026-06-02"],
        ["ENC1003", "P902", "", "DEPT_MED", "320.00", "2026-06-02"],  # Self-pay, empty plan_id
        ["ENC1004", "P903", "PLAN_SILVER", "DEPT_ER", "-50.00", "2026-06-03"],  # Anomaly: Negative billing
        ["ENC1005", "", "PLAN_BLUE", "DEPT_PED", "150.25", "2026-06-04"],  # Anomaly: Missing patient_id
    ]
    
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Loop over the pool to inflate the file to our desired row count
        for i in range(num_rows):
            template = base_rows[i % len(base_rows)].copy()
            # Mutate the ID slightly so rows feel distinct
            if template[0]:
                template[0] = f"{template[0]}_{i}"
            writer.writerow(template)

if __name__ == "__main__":
    raw_data_path = Path("datapulse_engine/data/raw/encounters_raw.csv")
    create_mock_csv(raw_data_path, num_rows=500)
    print(f"[SUCCESS] Mock dataset created with 500 rows at: {raw_data_path}")