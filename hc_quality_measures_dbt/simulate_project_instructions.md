# 📊 Healthcare Quality Measures with dbt & DuckDB

This project demonstrates a modern data stack workflow using **dbt** for transformation and **DuckDB** as the analytical engine. It specifically focuses on calculating clinical quality measures, such as hypertension compliance.

---

## 🛠 Setup & Installation

### 1. Install dbt and DuckDB
The easiest way to get started is using Python's package manager. It is recommended to use a virtual environment.

```bash
# Install dbt with the DuckDB adapter
pip install dbt-duckdb

# Install DuckDB CLI (via Homebrew for Mac/Linux)
brew install duckdb
```

### 2. Environment Setup (Linux/Codespaces Only)
If you are working in a **GitHub Codespace**, run this to ensure Homebrew and its dependencies are configured:

```bash
# Add Homebrew to your PATH
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# Install essential build tools
sudo apt-get update && sudo apt-get install build-essential -y
brew install gcc
```

---

## 🚀 Running the Workflow

Follow these steps in order to initialize the database and run the transformations.

```bash
# 1. Install dbt packages (like dbt_expectations)
dbt deps

# 2. Load raw CSV data into DuckDB
dbt seed

# 3. Run all models and data quality tests
dbt build

# 4. (Optional) Generate and serve the documentation site
dbt docs generate
dbt docs serve
```

---

## 🦆 Data Analysis with DuckDB

After running `dbt build`, your transformed data is stored in `quality_measures.duckdb`. You can query it directly using the DuckDB CLI:

```bash
duckdb quality_measures.duckdb
```

### Useful SQL Queries

**Verify Results**
```sql
-- List all tables created by dbt
SHOW TABLES;

-- Preview the final hypertension reporting table
SELECT * FROM mrt_quality_measure__hypertension LIMIT 10;
```

**Calculate Clinical Compliance**
```sql
-- Get the compliance percentage for the hypertension cohort
SELECT 
    COUNT(*) as total_patients,
    SUM(compliant) as compliant_patients,
    ROUND(100.0 * SUM(compliant) / COUNT(*), 2) as compliance_percentage
FROM mrt_quality_measure__hypertension;
```

**Data Lineage Audit**
```sql
-- Check data volume by source system
SELECT source_system, COUNT(*) 
FROM mrt_vitals__vitals
GROUP BY source_system
ORDER BY 2 DESC;
```

> **Pro Tip:** To exit the DuckDB interface, type `.exit`.

---

## 📦 Project Structure
*   **`models/`**: SQL transformations and quality measure logic.
*   **`seeds/`**: Raw clinical data and sample patient sets.
*   **`packages.yml`**: Configurations for dbt extensions.
*   **`dbt_project.yml`**: Main configuration file for the dbt project.
