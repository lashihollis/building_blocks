Viewing the project contents and practicing with dbt:

dbt seed
add packages.yml file to add dbt expectations
dbt deps to install pakage
dbt build
dbt docs generate
dbt docs serve (to see data lineage and documentation in browser)

to use duckdb:
installl homebrew (https://brew.sh/)
==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /home/codespace/.bashrc
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"' >> /home/codespace/.bashrc
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"
- Install Homebrew's dependencies if you have sudo access:
    sudo apt-get install build-essential
  For more information, see:
    https://docs.brew.sh/Homebrew-on-Linux
- We recommend that you install GCC:
    brew install gcc
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh

brew install duckdb
go to your project folder ex. duckdb analytics_engineering_project.duckdb

Sample queries to run:

-- List all tables
SHOW TABLES;

-- Preview your quality measure results
SELECT * FROM mrt_quality_measure__hypertension;

-- Get the compliance percentage
SELECT 
    COUNT(*) as total_patients,
    SUM(compliant) as compliant_patients,
    ROUND(100.0 * SUM(compliant) / COUNT(*), 2) as compliance_percentage
FROM mrt_quality_measure__hypertension;

-- Check your vitals table
SELECT * FROM mrt_vitals__vitals LIMIT 10;

-- See which sources provided the most data
SELECT source_system, COUNT(*) 
FROM mrt_vitals__vitals
GROUP BY source_system;

-- Exit the CLI
.exit