# Healthcare Quality Measures dbt Project

This project builds a small healthcare analytics workflow with dbt and DuckDB. It generates mock clinical data, loads it into DuckDB, and runs a set of staging, intermediate, and mart models to calculate a hypertension quality-measure result.

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

## 3. Install the required Python packages

```bash
pip install 'dbt-duckdb>=1.8,<1.9' pandas numpy
```

This installs:
- dbt Core
- the DuckDB adapter for dbt
- pandas and numpy used by the data generation script

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
dbt seed --profiles-dir .
dbt build --profiles-dir .
```

These commands will:
- load the seed data into DuckDB
- create the dbt models and views
- run the data tests defined in the project

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
    ROUND(100.0 * SUM(compliant) / COUNT(*), 2) as compliance_percentage
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

Reinstall the project dependencies:

```bash
pip install 'dbt-duckdb>=1.8,<1.9' pandas numpy
```

### Deprecation warnings during `dbt deps` or `dbt build`

These warnings are not usually blockers. The project still runs successfully with the current package versions used here.

## Expected outcome

A successful run should finish with dbt reporting a build that passes its tests and produces the DuckDB database file with the transformed healthcare models.
