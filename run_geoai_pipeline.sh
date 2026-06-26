#!/bin/bash
# Master execution script for GarissaDRM GeoAI Pipeline

echo "================================================="
echo "   🌍 GARISSA SENTINEL GEOAI PIPELINE 🌍"
echo "================================================="

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "[STEP 1] Data Ingestion & Conversion..."
python 1_data_ingestion.py

echo ""
echo "[STEP 2] GEE Asset Upload Automation..."
python 2_gee_upload_automation.py

echo ""
echo "[STEP 3] Modeling & Looker Studio Export..."
# Note: 3_modeling_stubs.py contains the logic, 4_looker_export.py executes the export
python 4_looker_export.py

echo ""
echo "================================================="
echo "   ✅ PIPELINE COMPLETE!"
echo "   Check the OUTPUT folder for Looker Studio CSVs."
echo "================================================="
