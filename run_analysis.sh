#!/bin/bash
# Run all SNAP QC analyses in sequence

echo "============================================================================"
echo "SNAP Validation Lab - Full Analysis Pipeline"
echo "============================================================================"
echo ""

# Check data file exists
if [ ! -f "data/qc_pub_fy2023.csv" ]; then
    echo "ERROR: Data file not found!"
    echo "Expected: data/qc_pub_fy2023.csv"
    echo ""
    echo "Download from: https://www.fns.usda.gov/snap/qc-annual-reports"
    exit 1
fi

echo "1. Running basic QC data analysis..."
echo "============================================================================"
python3 analysis/analyze_qc_data.py
echo ""
echo ""

echo "2. Running error impact analysis..."
echo "============================================================================"
python3 analysis/analyze_error_impact.py
echo ""
echo ""

echo "3. Running error type analysis..."
echo "============================================================================"
python3 analysis/analyze_error_types.py
echo ""
echo ""

echo "============================================================================"
echo "Analysis complete!"
echo "============================================================================"
echo ""
echo "See docs/notes.md for detailed findings and methodology."
