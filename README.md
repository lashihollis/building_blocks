# Building Blocks

A portfolio of hands-on projects and exercises in analytics engineering, data
quality, Python, and SQL. Each folder is a separate project or area of practice;
there is no single environment or application to install for the whole repository.

## Projects

| Project | What it does |
|---|---|
| [`hc_quality_measures_dbt/`](./hc_quality_measures_dbt/) | A dbt and DuckDB workflow that generates mock patient data, combines payer, EHR, and patient-reported vitals, applies configured source precedence, and produces a hypertension quality-measure mart. |
| [`data_quality_checker_py/`](./data_quality_checker_py/) | A Python data-quality framework demonstrating reusable checks, structured failure results, and a Matplotlib visualization on simulated claims data. |
| [`finance_ingestion_pipeline/`](./finance_ingestion_pipeline/) | A learning project for selecting files to process, skip, or investigate using status metadata, checksums, and heartbeat age. Includes pytest coverage; it does not ingest transaction rows or run a production pipeline. |
| [`python_practice/`](./python_practice/) | Standalone Python exercises, small scripts, notebooks, and data-analysis projects, including census-data cleaning and exploratory analysis. |
| [`sql_practice/`](./sql_practice/) | Standalone SQL exercises for querying, analysis, and database setup. |
| [`case_studies/`](./case_studies/) | Written project narratives covering healthcare quality-measure modeling and gaps-in-care work. |

## Getting started

Choose a project folder and follow its README for project-specific setup. For
example, to build the healthcare quality-measure project:

```bash
cd hc_quality_measures_dbt
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
dbt deps
python generate_data.py
dbt build --profiles-dir .
```

The dbt build loads the project seeds, builds the staging, intermediate, and mart
models, and runs the configured source, seed, and selected mart tests. The result
is written to `hc_quality_measures_dbt/quality_measures.duckdb`. See the
[healthcare project README](./hc_quality_measures_dbt/README.md) for details.

The financial file-tracker tests can be run separately:

```bash
cd finance_ingestion_pipeline
python -m pip install pytest
python -m pytest -v
```

## Automation

GitHub Actions workflows in [`.github/workflows/`](./.github/workflows/) can
refresh the generated healthcare data and then run the dbt build. These
workflows support scheduled and manual runs; they are specific to that project
and do not provide repository-wide CI for every exercise.

## Technologies and topics

- **Python** for scripts, data generation, reusable validation logic, and
  notebooks
- **SQL and dbt** for transformations, model lineage, and data-quality checks
- **DuckDB** for local analytical storage
- **Jupyter** for exploratory data analysis
- **pytest and GitHub Actions** for project-level automated tests and workflow
  automation

## Repository status

This is an evolving learning portfolio. Projects vary in maturity and scope:
some are executable code with tests, while others are exercises or written
case studies. Refer to each project’s documentation for its current
dependencies, setup steps, and limitations.
