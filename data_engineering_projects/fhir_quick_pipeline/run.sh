#!/bin/bash
echo "🚀 Starting FHIR Pipeline..."

# Fetch data
python scripts/fetch_fhir.py

# Transform to CSV
python scripts/transform_to_csv.py

# Load to DuckDB
python scripts/run_pipeline.py

echo "✅ Pipeline complete!"
