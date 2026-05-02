#!/bin/bash

echo "🚀 Starting FHIR Pipeline"
echo "========================="

# Step 1: Fetch FHIR data
echo ""
echo "📡 Step 1: Fetching data from FHIR API..."
python scripts/fetch_fhir.py

# Step 2: Transform to CSV
echo ""
echo "🔄 Step 2: Transforming to CSV..."
python scripts/transform_to_csv.py

# Step 3: Load to DuckDB
echo ""
echo "💾 Step 3: Loading to DuckDB..."
python scripts/load_to_duckdb.py

echo ""
echo "✅ Pipeline complete!"
echo ""
echo "To explore the data:"
echo "  duckdb fhir_data.duckdb"
echo ""
echo "Try these queries:"
echo "  SELECT * FROM patients LIMIT 5;"
echo "  SELECT * FROM vitals LIMIT 10;"
echo "  SELECT vital_type, COUNT(*) FROM vitals GROUP BY vital_type;"
