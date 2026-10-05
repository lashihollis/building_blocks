# Healthcare Quality Measures dbt Project

This project builds a small healthcare analytics workflow with dbt and DuckDB. It generates mock clinical data, loads it into DuckDB, and runs staging, intermediate, and mart models to calculate a hypertension quality-measure result. Vital-source precedence is configured in the `source_priority` seed; the vitals mart keeps one preferred source per patient, measurement date, and vital type.

The hypertension mart reports one row per patient with a hypertension diagnosis and marks a patient compliant when at least one systolic or diastolic blood-pressure component was recorded in the six calendar months through `measure_as_of_date`. The as-of date is recorded in the output, and future-dated vitals are excluded.

## What you need

- Python 3.10 or newer
- pip
- Git
- A terminal with internet access to install Python packages

> This project does not require Homebrew for setup. On Linux, Codespaces, or other non-macOS environments, the Python-based workflow below is the recommended path.

## 1. Open the project folder

```bash
cd /path/to/building_blocks/hc_quality_measures_dbt
```

## 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## 3. Install the project dependencies

```bash
python -m pip install -r requirements.txt
```

The requirements file installs dbt Core, the DuckDB adapter, and the pandas and
numpy dependencies used by the data generator.

## 4. Install dbt packages declared by the project

```bash
dbt deps
```

If you run dbt from outside the project directory, use:

```bash
dbt deps --project-dir .
```

## 5. Generate the mock healthcare data

```bash
python generate_data.py
```

This writes the seed CSVs used by the dbt project into the seeds folder.

## 6. Load the seed data and build the models

```bash
dbt build --profiles-dir .
```

This command will:
- load the seed data into DuckDB
- create the dbt models and views
- run the data tests defined for the input sources and critical mart outputs

## Data quality tests

Tests are concentrated at the input boundary: external source CSVs are checked in
`models/sources.yml`, while the `payer_data`, `ehr_data`, `patient_reported_data`,
`seed_patients`, and lookup seeds are checked in `seeds/_seeds.yml`. This catches
missing IDs, invalid vital values, and references to unknown patients, diagnosis
codes, or source systems before downstream models consume the data.

Staging and intermediate models are simple renames, filters, and unions, so
repeating the same null, accepted-value, and relationship tests on every layer
adds runtime without much additional protection. The marts retain focused checks
for their output grain and the hypertension compliance calculation because those
are important reporting contracts rather than repeated input checks.

## 7. Optional: generate and serve dbt docs

```bash
dbt docs generate --profiles-dir .
dbt docs serve
```

## 8. Inspect the results

After a successful build, the database file will be created at:

```text
quality_measures.duckdb
```

You can inspect the generated tables with DuckDB. If the DuckDB CLI is available on your machine, run:

```bash
duckdb quality_measures.duckdb
```

### Example SQL queries

Verify the tables created by dbt:

```sql
SHOW TABLES;
```

Preview the final hypertension reporting table:

```sql
SELECT * FROM mrt_quality_measure__hypertension LIMIT 10;
```

Calculate the clinical compliance percentage for the hypertension cohort:

```sql
SELECT 
    COUNT(*) as total_patients,
    SUM(compliant) as compliant_patients,
    ROUND(100.0 * SUM(compliant) / NULLIF(COUNT(*), 0), 2) as compliance_percentage
FROM mrt_quality_measure__hypertension;
```

Audit data volume by source system:

```sql
SELECT source_system, COUNT(*)
FROM mrt_vitals__vitals
GROUP BY source_system
ORDER BY 2 DESC;
```

> To exit the DuckDB interface, type `.exit`.

## Common troubleshooting

### `dbt: command not found`

Make sure your virtual environment is active:

```bash
source .venv/bin/activate
```

If needed, use the venv binary directly:

```bash
.venv/bin/dbt --version
```

### `No profiles.yml found`

Run the commands from the project directory or pass the project profile directory explicitly:

```bash
dbt build --profiles-dir .
```

### `ModuleNotFoundError` for pandas or numpy

Reinstall the project dependencies from the project directory:

```bash
python -m pip install -r requirements.txt
```

### Deprecation warnings during `dbt deps` or `dbt build`

These warnings are not usually blockers. The project still runs successfully with the current package versions used here.

## Expected outcome

A successful run should finish with dbt reporting a build that passes its tests and produces the DuckDB database file with the transformed healthcare models.
