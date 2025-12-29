#!/usr/bin/env python3
"""
Analyze specific error types in SNAP benefit calculations
Focus on income reporting vs deduction calculation errors

Input: qc_pub_fy2023.csv - SNAP Quality Control microdata
Output: Detailed breakdown of income vs deduction errors, complexity patterns

Key Question: Are errors driven by income verification failures or
              deduction calculation mistakes?
"""

import pandas as pd
import numpy as np
import os

def analyze_error_types():
    """
    Deep dive into income and deduction errors

    Analyzes:
    - Income sources (wages, SSI, Social Security, etc.) by error type
    - Deduction types (shelter, medical, earned income, etc.) by error type
    - Income complexity (number of sources) vs error rate
    - Calculation flow: gross income → deductions → net income → benefit
    - High-risk profiles for targeting QC resources
    """

    # =================================================================
    # INPUT VALIDATION
    # =================================================================

    input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'qc_pub_fy2023.csv')
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Required input file not found: {input_file}")

    print("Loading QC data...")
    df = pd.read_csv(input_file)

    # Validate required columns for income/deduction analysis
    required_columns = [
        'STATENAME', 'STATUS',
        'FSWAGES', 'FSSLFEMP', 'FSSOCSEC', 'FSSSI', 'FSCSUPRT',  # Income sources
        'FSGRINC', 'FSNETINC', 'FSBEN',  # Income and benefits
        'FSSTDDED', 'FSERNDED', 'FSDEPDED', 'FSMEDDED', 'SHELDED', 'FSTOTDED'  # Deductions
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns for income/deduction analysis: {missing_columns}\n"
            f"This analysis requires detailed income and deduction variables."
        )

    # Filter to Mississippi
    ms_df = df[df['STATENAME'] == 'Mississippi'].copy()

    if len(ms_df) == 0:
        raise ValueError("No Mississippi data found!")

    # Validate numeric columns are actually numeric
    numeric_cols = ['FSGRINC', 'FSNETINC', 'FSBEN', 'FSTOTDED']
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(ms_df[col]):
            raise ValueError(f"Column {col} should be numeric but isn't")

    # Define case types
    correct_cases = ms_df[ms_df['STATUS'] == 1]
    payment_errors = ms_df[ms_df['STATUS'] == 2]
    error_cases = ms_df[ms_df['STATUS'] == 3]

    print("=" * 80)
    print("DETAILED ERROR TYPE ANALYSIS - INCOME VS DEDUCTIONS")
    print("Mississippi SNAP QC Data FY 2023")
    print("=" * 80)

    # Income source analysis
    print("\n" + "=" * 80)
    print("INCOME SOURCES BY CASE TYPE")
    print("=" * 80)

    income_sources = {
        'FSWAGES': 'Wages/Salary',
        'FSSLFEMP': 'Self-Employment',
        'FSSOCSEC': 'Social Security',
        'FSSSI': 'SSI',
        'FSUNEMP': 'Unemployment',
        'FSVET': 'Veterans Benefits',
        'FSTANF': 'TANF',
        'FSCSUPRT': 'Child Support'
    }

    for col, label in income_sources.items():
        if col in ms_df.columns:
            print(f"\n{label} ({col}):")
            for name, subset in [("Correct", correct_cases),
                                ("Payment Error", payment_errors),
                                ("Error Case", error_cases)]:
                has_income = len(subset[subset[col] > 0])
                pct = 100 * has_income / len(subset) if len(subset) > 0 else 0
                avg_amt = subset[subset[col] > 0][col].mean() if has_income > 0 else 0
                print(f"  {name:15s}: {has_income:3d} cases ({pct:5.1f}%) - Avg: ${avg_amt:.2f}")

    # Gross income comparison
    print("\n" + "=" * 80)
    print("GROSS INCOME ANALYSIS")
    print("=" * 80)

    for name, subset in [("Correct Cases", correct_cases),
                          ("Payment Errors", payment_errors),
                          ("Error Cases", error_cases)]:
        print(f"\n{name}:")
        if 'FSGRINC' in subset.columns:
            print(f"  Average gross income: ${subset['FSGRINC'].mean():.2f}")
            print(f"  Median gross income: ${subset['FSGRINC'].median():.2f}")
            zero_income = len(subset[subset['FSGRINC'] == 0])
            print(f"  Cases with $0 gross income: {zero_income} ({100*zero_income/len(subset):.1f}%)")

    # Deduction analysis
    print("\n" + "=" * 80)
    print("DEDUCTION ANALYSIS BY CASE TYPE")
    print("=" * 80)

    deductions = {
        'FSSTDDED': 'Standard Deduction',
        'FSERNDED': 'Earned Income Deduction',
        'FSDEPDED': 'Dependent Care Deduction',
        'FSMEDDED': 'Medical Deduction',
        'SHELDED': 'Shelter Deduction',
        'FSTOTDED': 'Total Deductions'
    }

    for col, label in deductions.items():
        if col in ms_df.columns:
            print(f"\n{label} ({col}):")
            for name, subset in [("Correct", correct_cases),
                                ("Payment Error", payment_errors),
                                ("Error Case", error_cases)]:
                has_deduction = len(subset[subset[col] > 0])
                pct = 100 * has_deduction / len(subset) if len(subset) > 0 else 0
                avg_amt = subset[subset[col] > 0][col].mean() if has_deduction > 0 else 0
                print(f"  {name:15s}: {has_deduction:3d} cases ({pct:5.1f}%) - Avg: ${avg_amt:.2f}")

    # Net income comparison
    print("\n" + "=" * 80)
    print("NET INCOME ANALYSIS")
    print("=" * 80)

    for name, subset in [("Correct Cases", correct_cases),
                          ("Payment Errors", payment_errors),
                          ("Error Cases", error_cases)]:
        print(f"\n{name}:")
        if 'FSNETINC' in subset.columns:
            print(f"  Average net income: ${subset['FSNETINC'].mean():.2f}")
            print(f"  Median net income: ${subset['FSNETINC'].median():.2f}")
            zero_net = len(subset[subset['FSNETINC'] == 0])
            print(f"  Cases with $0 net income: {zero_net} ({100*zero_net/len(subset):.1f}%)")

    # Calculation flow analysis
    print("\n" + "=" * 80)
    print("BENEFIT CALCULATION FLOW ANALYSIS")
    print("=" * 80)

    # =================================================================
    # SANITY CHECKS ON CALCULATION FLOW
    # =================================================================

    # SNAP benefit calculation: Gross Income - Deductions = Net Income
    # Net income determines benefit amount
    # This relationship should hold for all cases (allowing for rounding)

    if all(col in ms_df.columns for col in ['FSGRINC', 'FSTOTDED', 'FSNETINC']):
        # Calculate expected net income
        expected_net = ms_df['FSGRINC'] - ms_df['FSTOTDED']
        actual_net = ms_df['FSNETINC']

        # Allow $5 difference for rounding/minor adjustments
        large_discrepancies = abs(expected_net - actual_net) > 5
        if large_discrepancies.sum() > len(ms_df) * 0.1:  # More than 10% have issues
            print(f"WARNING: {large_discrepancies.sum()} cases have large net income discrepancies")
            print(f"  This suggests data quality issues or complex deduction rules")

    # Create a comparison of gross → net → benefit
    if all(col in ms_df.columns for col in ['FSGRINC', 'FSTOTDED', 'FSNETINC', 'FSBEN']):
        print("\nAverage Calculation Flow:")
        print(f"{'Case Type':<20} {'Gross Income':<15} {'Deductions':<15} {'Net Income':<15} {'Benefit':<15}")
        print("-" * 80)

        for name, subset in [("Correct Cases", correct_cases),
                            ("Payment Errors", payment_errors),
                            ("Error Cases", error_cases)]:
            gross = subset['FSGRINC'].mean()
            deduct = subset['FSTOTDED'].mean()
            net = subset['FSNETINC'].mean()
            benefit = subset['FSBEN'].mean()
            print(f"{name:<20} ${gross:<14.2f} ${deduct:<14.2f} ${net:<14.2f} ${benefit:<14.2f}")

    # Income complexity analysis
    print("\n" + "=" * 80)
    print("INCOME COMPLEXITY AND ERROR RATES")
    print("=" * 80)

    # Count number of income sources per household
    income_cols = [col for col in income_sources.keys() if col in ms_df.columns]

    ms_df['num_income_sources'] = (ms_df[income_cols] > 0).sum(axis=1)

    print("\nError rate by number of income sources:")
    for num_sources in sorted(ms_df['num_income_sources'].unique()):
        source_df = ms_df[ms_df['num_income_sources'] == num_sources]
        error_count = len(source_df[source_df['STATUS'].isin([2, 3])])
        error_rate = 100 * error_count / len(source_df)
        print(f"  {num_sources} income source(s): {error_rate:.1f}% error rate ({error_count}/{len(source_df)} cases)")

    # Specific error patterns
    print("\n" + "=" * 80)
    print("COMMON ERROR PATTERNS")
    print("=" * 80)

    # Pattern 1: Earned income cases
    if 'FSWAGES' in ms_df.columns:
        earned_income_cases = ms_df[ms_df['FSWAGES'] > 0]
        earned_error_rate = 100 * len(earned_income_cases[earned_income_cases['STATUS'].isin([2, 3])]) / len(earned_income_cases)
        no_earned = ms_df[ms_df['FSWAGES'] == 0]
        no_earned_error_rate = 100 * len(no_earned[no_earned['STATUS'].isin([2, 3])]) / len(no_earned)

        print(f"\nEarned Income:")
        print(f"  With wages: {earned_error_rate:.1f}% error rate")
        print(f"  Without wages: {no_earned_error_rate:.1f}% error rate")
        print(f"  Difference: {earned_error_rate - no_earned_error_rate:+.1f} percentage points")

    # Pattern 2: Medical deductions
    if 'FSMEDDED' in ms_df.columns:
        with_med = ms_df[ms_df['FSMEDDED'] > 0]
        med_error_rate = 100 * len(with_med[with_med['STATUS'].isin([2, 3])]) / len(with_med)
        no_med = ms_df[ms_df['FSMEDDED'] == 0]
        no_med_error_rate = 100 * len(no_med[no_med['STATUS'].isin([2, 3])]) / len(no_med)

        print(f"\nMedical Deductions:")
        print(f"  With medical deduction: {med_error_rate:.1f}% error rate")
        print(f"  Without medical deduction: {no_med_error_rate:.1f}% error rate")
        print(f"  Difference: {med_error_rate - no_med_error_rate:+.1f} percentage points")

    # Pattern 3: Shelter costs
    if 'SHELDED' in ms_df.columns:
        with_shelter = ms_df[ms_df['SHELDED'] > 0]
        shelter_error_rate = 100 * len(with_shelter[with_shelter['STATUS'].isin([2, 3])]) / len(with_shelter)
        no_shelter = ms_df[ms_df['SHELDED'] == 0]
        no_shelter_error_rate = 100 * len(no_shelter[no_shelter['STATUS'].isin([2, 3])]) / len(no_shelter)

        print(f"\nShelter Deductions:")
        print(f"  With shelter deduction: {shelter_error_rate:.1f}% error rate")
        print(f"  Without shelter deduction: {no_shelter_error_rate:.1f}% error rate")
        print(f"  Difference: {shelter_error_rate - no_shelter_error_rate:+.1f} percentage points")

    # Most error-prone combinations
    print("\n" + "=" * 80)
    print("HIGHEST RISK PROFILES")
    print("=" * 80)

    # Complex income + high deductions
    if all(col in ms_df.columns for col in ['num_income_sources', 'FSTOTDED']):
        high_deduct = ms_df['FSTOTDED'] > ms_df['FSTOTDED'].median()
        complex_income = ms_df['num_income_sources'] >= 2

        high_risk = ms_df[high_deduct & complex_income]
        high_risk_error_rate = 100 * len(high_risk[high_risk['STATUS'].isin([2, 3])]) / len(high_risk) if len(high_risk) > 0 else 0

        low_risk = ms_df[~high_deduct & ~complex_income]
        low_risk_error_rate = 100 * len(low_risk[low_risk['STATUS'].isin([2, 3])]) / len(low_risk) if len(low_risk) > 0 else 0

        print(f"\nComplex cases (2+ income sources AND above-median deductions):")
        print(f"  Error rate: {high_risk_error_rate:.1f}% ({len(high_risk)} cases)")

        print(f"\nSimple cases (0-1 income sources AND below-median deductions):")
        print(f"  Error rate: {low_risk_error_rate:.1f}% ({len(low_risk)} cases)")

        print(f"\nRisk difference: {high_risk_error_rate - low_risk_error_rate:+.1f} percentage points")

    return ms_df, correct_cases, payment_errors, error_cases

if __name__ == "__main__":
    ms_df, correct, payment_err, error = analyze_error_types()
