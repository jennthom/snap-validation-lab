#!/usr/bin/env python3
"""
Analyze SNAP QC data for Mississippi
Compares actual SNAP participant characteristics with Census estimates

Input: qc_pub_fy2023.csv - SNAP Quality Control microdata from USDA FNS
Output: Printed summary statistics and demographic breakdowns
"""

import pandas as pd
import numpy as np
import os

def analyze_ms_snap_qc():
    """
    Analyze Mississippi SNAP QC microdata

    Validates data quality and produces summary statistics on:
    - Household characteristics (size, income, poverty status)
    - SNAP benefit amounts
    - Case error rates
    - Demographic indicators
    """

    # =================================================================
    # INPUT VALIDATION
    # =================================================================

    # Check that input file exists
    # Look for data file in data/ directory (relative to project root)
    input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'qc_pub_fy2023.csv')
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Required input file not found: {input_file}\n"
            f"Expected location: data/qc_pub_fy2023.csv\n"
            f"Download from: https://www.fns.usda.gov/snap/qc-annual-reports"
        )

    # Load data
    print("Loading QC data...")
    df = pd.read_csv(input_file)

    # Validate required columns exist
    required_columns = ['STATENAME', 'STATE', 'RAWHSIZE', 'TPOV', 'FSBEN', 'STATUS']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}\n"
            f"This may not be a valid SNAP QC file."
        )

    # Filter to Mississippi
    ms_df = df[df['STATENAME'] == 'Mississippi'].copy()

    # Validate we have Mississippi data
    if len(ms_df) == 0:
        raise ValueError(
            "No Mississippi data found in QC file!\n"
            f"Available states: {sorted(df['STATENAME'].unique())[:10]}..."
        )

    # Sanity check: should have at least 100 cases (typically 1000+)
    if len(ms_df) < 100:
        print(f"WARNING: Only {len(ms_df)} MS cases found. Expected 1000+. Data may be incomplete.")

    # Validate data ranges
    assert ms_df['RAWHSIZE'].min() >= 1, "Invalid household size: must be >= 1"
    assert ms_df['RAWHSIZE'].max() <= 20, "Suspicious household size: > 20 people"
    assert ms_df['TPOV'].min() >= 0, "Invalid poverty ratio: cannot be negative"
    assert ms_df['TPOV'].max() <= 1000, "Suspicious poverty ratio: > 1000%"
    assert ms_df['FSBEN'].min() >= 0, "Invalid benefit amount: cannot be negative"
    assert ms_df['STATUS'].isin([1, 2, 3]).all(), "Invalid STATUS values: must be 1, 2, or 3"

    print("=" * 70)
    print("MISSISSIPPI SNAP QC ANALYSIS (FY 2023)")
    print("=" * 70)

    # Basic stats
    print(f"\nSample Size: {len(ms_df)} households")
    print(f"Average household size: {ms_df['RAWHSIZE'].mean():.2f}")
    print(f"Total persons in sample: {ms_df['RAWHSIZE'].sum()}")

    # Income/Poverty Distribution
    print("\n" + "=" * 70)
    print("INCOME TO POVERTY RATIO DISTRIBUTION")
    print("=" * 70)

    poverty_bins = [
        (0, 50, "Below 50% poverty"),
        (50, 100, "50-100% poverty"),
        (100, 130, "100-130% poverty (SNAP eligible)"),
        (130, 200, "Above 130% poverty")
    ]

    for min_val, max_val, label in poverty_bins:
        count = len(ms_df[(ms_df['TPOV'] >= min_val) & (ms_df['TPOV'] < max_val)])
        pct = 100 * count / len(ms_df)
        print(f"{label:40s}: {count:4d} ({pct:5.1f}%)")

    # SNAP Benefits
    print("\n" + "=" * 70)
    print("SNAP BENEFIT AMOUNTS")
    print("=" * 70)
    print(f"Average monthly benefit: ${ms_df['FSBEN'].mean():.2f}")
    print(f"Median monthly benefit: ${ms_df['FSBEN'].median():.2f}")
    print(f"Total monthly benefits (sample): ${ms_df['FSBEN'].sum():,.2f}")

    # Household characteristics
    print("\n" + "=" * 70)
    print("HOUSEHOLD SIZE DISTRIBUTION")
    print("=" * 70)
    for size in sorted(ms_df['RAWHSIZE'].unique()):
        count = len(ms_df[ms_df['RAWHSIZE'] == size])
        pct = 100 * count / len(ms_df)
        print(f"{size} person(s): {count:4d} ({pct:5.1f}%)")

    # Case status (quality control findings)
    print("\n" + "=" * 70)
    print("CASE STATUS (Quality Control Findings)")
    print("=" * 70)
    status_labels = {1: "Active - Correct", 2: "Active - Payment Error", 3: "Error Case"}
    for status in sorted(ms_df['STATUS'].unique()):
        count = len(ms_df[ms_df['STATUS'] == status])
        pct = 100 * count / len(ms_df)
        label = status_labels.get(status, f"Unknown ({status})")
        print(f"{label:30s}: {count:4d} ({pct:5.1f}%)")

    # Calculate error rate
    error_cases = len(ms_df[ms_df['STATUS'].isin([2, 3])])
    error_rate = 100 * error_cases / len(ms_df)
    print(f"\nOverall error rate: {error_rate:.1f}%")

    # =================================================================
    # SANITY CHECKS ON CALCULATIONS
    # =================================================================

    # Check that status percentages sum to 100%
    status_counts = ms_df['STATUS'].value_counts()
    total_pct = 100 * status_counts.sum() / len(ms_df)
    assert abs(total_pct - 100) < 0.1, f"Status percentages don't sum to 100%: {total_pct:.1f}%"

    # Check poverty distribution sums to 100%
    poverty_total = sum(len(ms_df[(ms_df['TPOV'] >= min_val) & (ms_df['TPOV'] < max_val)])
                       for min_val, max_val, _ in poverty_bins)
    poverty_pct = 100 * poverty_total / len(ms_df)
    assert abs(poverty_pct - 100) < 1.0, f"Poverty bins don't cover all cases: {poverty_pct:.1f}%"

    # Key demographic indicators
    print("\n" + "=" * 70)
    print("KEY DEMOGRAPHIC INDICATORS")
    print("=" * 70)

    # Elderly, disabled, children
    if 'FSELDER' in ms_df.columns:
        elderly = len(ms_df[ms_df['FSELDER'] > 0])
        print(f"Households with elderly: {elderly} ({100*elderly/len(ms_df):.1f}%)")

    if 'FSDIS' in ms_df.columns:
        disabled = len(ms_df[ms_df['FSDIS'] > 0])
        print(f"Households with disabled: {disabled} ({100*disabled/len(ms_df):.1f}%)")

    if 'FSKID' in ms_df.columns:
        with_kids = len(ms_df[ms_df['FSKID'] > 0])
        print(f"Households with children: {with_kids} ({100*with_kids/len(ms_df):.1f}%)")

    print("\n" + "=" * 70)
    print("COMPARISON TO CENSUS ESTIMATES")
    print("=" * 70)
    print("\nCensus estimates for MS counties:")
    print("  Hinds County: 28.7% eligible (130% FPL)")
    print("  Bolivar County: 43.5% eligible (130% FPL)")
    print("\nQC data shows:")
    eligible = len(ms_df[ms_df['TPOV'] <= 130])
    print(f"  {100*eligible/len(ms_df):.1f}% of participants at or below 130% FPL")
    print(f"  {100*error_rate:.1f}% error rate in benefit calculations")

    return ms_df

if __name__ == "__main__":
    ms_data = analyze_ms_snap_qc()
