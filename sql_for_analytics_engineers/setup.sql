-- ============================================================
-- SQL Course Database Setup
-- ============================================================
-- Run this file from the root (sql_for_analytics_engineers) of the repository with:
--
-- duckdb course.duckdb
-- .read setup.sql
--
-- The CSV paths are relative to the directory where DuckDB
-- was opened.
-- ============================================================


-- Create the patients table.
CREATE OR REPLACE TABLE patients AS
SELECT *
FROM read_csv_auto(
    'data/patients.csv',
    header = true
);


-- Create the providers table.
CREATE OR REPLACE TABLE providers AS
SELECT *
FROM read_csv_auto(
    'data/providers.csv',
    header = true
);


-- Create the visits table.
CREATE OR REPLACE TABLE visits AS
SELECT *
FROM read_csv_auto(
    'data/visits.csv',
    header = true
);


-- Create the claims table.
CREATE OR REPLACE TABLE claims AS
SELECT *
FROM read_csv_auto(
    'data/claims.csv',
    header = true
);


-- ============================================================
-- Confirm that the tables were created.
-- ============================================================

SHOW TABLES;


-- ============================================================
-- Confirm that data was loaded into each table.
-- ============================================================

SELECT
    'patients' AS table_name,
    COUNT(*) AS row_count
FROM patients

UNION ALL

SELECT
    'providers' AS table_name,
    COUNT(*) AS row_count
FROM providers

UNION ALL

SELECT
    'visits' AS table_name,
    COUNT(*) AS row_count
FROM visits

UNION ALL

SELECT
    'claims' AS table_name,
    COUNT(*) AS row_count
FROM claims;
