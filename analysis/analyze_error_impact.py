#!/usr/bin/env python3
"""
Quantify administrative error impact on SNAP benefit accuracy
Analyzes QC data to understand magnitude and patterns of errors

Input: qc_pub_fy2023.csv - SNAP Quality Control microdata
Output: Detailed error analysis including financial impact and error patterns
"""

import pandas as pd
import numpy as np
import os

def analyze_error_impact():
    """
    Analyze administrative error impact on benefit accuracy

    Breaks down errors by:
    - Type (payment errors vs error cases)
    - Household characteristics (size, poverty level, composition)
    - Financial impact (over/under payment amounts)
    - Projected statewide impact
    """

    # =================================================================
    # INPUT VALIDATION
    # =================================================================

    input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'qc_pub_fy2023.csv')
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Required input file not found: {input_file}")

    print("Loading QC data...")
    df = pd.read_csv(input_file)

    # Validate required columns for error analysis
    required_columns = [
        'STATENAME', 'STATUS', 'FSBEN', 'RAWHSIZE', 'TPOV',
        'FSELDER', 'FSDIS', 'FSKID'
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for error analysis: {missing_columns}")

    # Filter to Mississippi
    ms_df = df[df['STATENAME'] == 'Mississippi'].copy()

    if len(ms_df) == 0:
        raise ValueError("No Mississippi data found!")

    # Validate STATUS values (1=Correct, 2=Payment Error, 3=Error Case)
    valid_status = [1, 2, 3]
    if not ms_df['STATUS'].isin(valid_status).all():
        invalid = ms_df[~ms_df['STATUS'].isin(valid_status)]['STATUS'].unique()
        raise ValueError(f"Invalid STATUS values found: {invalid}. Expected: {valid_status}")

    print("=" * 80)
    print("ADMINISTRATIVE ERROR IMPACT ANALYSIS")
    print("SNAP Quality Control Data - Mississippi FY 2023")
    print("=" * 80)

    # Define case types
    correct_cases = ms_df[ms_df['STATUS'] == 1]
    payment_errors = ms_df[ms_df['STATUS'] == 2]
    error_cases = ms_df[ms_df['STATUS'] == 3]

    print(f"\nSample breakdown:")
    print(f"  Total cases: {len(ms_df)}")
    print(f"  Correct cases: {len(correct_cases)} ({100*len(correct_cases)/len(ms_df):.1f}%)")
    print(f"  Payment errors: {len(payment_errors)} ({100*len(payment_errors)/len(ms_df):.1f}%)")
    print(f"  Error cases: {len(error_cases)} ({100*len(error_cases)/len(ms_df):.1f}%)")

    # =================================================================
    # SANITY CHECKS
    # =================================================================

    # Verify all cases are classified (should sum to total)
    total_classified = len(correct_cases) + len(payment_errors) + len(error_cases)
    assert total_classified == len(ms_df), \
        f"Case counts don't match total: {total_classified} != {len(ms_df)}"

    # Check percentages sum to 100%
    total_pct = (100*len(correct_cases)/len(ms_df) +
                100*len(payment_errors)/len(ms_df) +
                100*len(error_cases)/len(ms_df))
    assert abs(total_pct - 100) < 0.1, f"Percentages don't sum to 100%: {total_pct:.1f}%"

    # Benefit amount analysis
    print("\n" + "=" * 80)
    print("BENEFIT AMOUNT ANALYSIS BY CASE TYPE")
    print("=" * 80)

    for name, subset in [("Correct Cases", correct_cases),
                          ("Payment Errors", payment_errors),
                          ("Error Cases", error_cases)]:
        print(f"\n{name}:")
        print(f"  Average benefit: ${subset['FSBEN'].mean():.2f}")
        print(f"  Median benefit: ${subset['FSBEN'].median():.2f}")
        print(f"  Total monthly: ${subset['FSBEN'].sum():,.2f}")
        print(f"  Min benefit: ${subset['FSBEN'].min():.2f}")
        print(f"  Max benefit: ${subset['FSBEN'].max():.2f}")

    # Financial impact of errors
    print("\n" + "=" * 80)
    print("FINANCIAL IMPACT OF ERRORS")
    print("=" * 80)

    # Compare error cases to correct cases
    correct_avg = correct_cases['FSBEN'].mean()
    payment_error_avg = payment_errors['FSBEN'].mean()
    error_case_avg = error_cases['FSBEN'].mean()

    payment_error_diff = payment_error_avg - correct_avg
    error_case_diff = error_case_avg - correct_avg

    print(f"\nAverage benefit comparison:")
    print(f"  Correct cases: ${correct_avg:.2f}")
    print(f"  Payment errors: ${payment_error_avg:.2f} ({payment_error_diff:+.2f} difference)")
    print(f"  Error cases: ${error_case_avg:.2f} ({error_case_diff:+.2f} difference)")

    # Estimate monthly overpayment/underpayment
    total_error_amount = (len(payment_errors) * payment_error_diff +
                         len(error_cases) * error_case_diff)

    print(f"\nEstimated monthly impact (sample):")
    print(f"  Payment errors: {len(payment_errors)} cases × ${payment_error_diff:.2f} = ${len(payment_errors) * payment_error_diff:,.2f}")
    print(f"  Error cases: {len(error_cases)} cases × ${error_case_diff:.2f} = ${len(error_cases) * error_case_diff:,.2f}")
    print(f"  Total monthly impact: ${total_error_amount:,.2f}")

    # Error rates by household characteristics
    print("\n" + "=" * 80)
    print("ERROR RATES BY HOUSEHOLD CHARACTERISTICS")
    print("=" * 80)

    # By household size
    print("\nBy Household Size:")
    for size in sorted(ms_df['RAWHSIZE'].unique()):
        size_df = ms_df[ms_df['RAWHSIZE'] == size]
        error_count = len(size_df[size_df['STATUS'].isin([2, 3])])
        error_rate = 100 * error_count / len(size_df)
        print(f"  {size} person(s): {error_rate:.1f}% error rate ({error_count}/{len(size_df)} cases)")

    # By poverty level
    print("\nBy Income to Poverty Ratio:")
    poverty_ranges = [
        (0, 50, "Below 50% poverty"),
        (50, 100, "50-100% poverty"),
        (100, 130, "100-130% poverty"),
        (130, 200, "Above 130% poverty")
    ]

    for min_pov, max_pov, label in poverty_ranges:
        pov_df = ms_df[(ms_df['TPOV'] >= min_pov) & (ms_df['TPOV'] < max_pov)]
        if len(pov_df) > 0:
            error_count = len(pov_df[pov_df['STATUS'].isin([2, 3])])
            error_rate = 100 * error_count / len(pov_df)
            print(f"  {label}: {error_rate:.1f}% error rate ({error_count}/{len(pov_df)} cases)")

    # By household composition
    print("\nBy Household Composition:")
    for col, label in [('FSELDER', 'With elderly'),
                       ('FSDIS', 'With disabled'),
                       ('FSKID', 'With children')]:
        if col in ms_df.columns:
            with_char = ms_df[ms_df[col] > 0]
            without_char = ms_df[ms_df[col] == 0]

            with_error_rate = 100 * len(with_char[with_char['STATUS'].isin([2, 3])]) / len(with_char)
            without_error_rate = 100 * len(without_char[without_char['STATUS'].isin([2, 3])]) / len(without_char)

            print(f"  {label}: {with_error_rate:.1f}% error rate")
            print(f"  Without: {without_error_rate:.1f}% error rate")

    # Projected statewide impact
    print("\n" + "=" * 80)
    print("PROJECTED STATEWIDE IMPACT (Mississippi)")
    print("=" * 80)

    # Mississippi had approximately 369,000 SNAP households in 2023
    # This is an estimate - adjust based on actual admin data
    ms_snap_households = 369000

    sample_error_rate = len(ms_df[ms_df['STATUS'].isin([2, 3])]) / len(ms_df)
    projected_error_cases = ms_snap_households * sample_error_rate

    avg_error_impact = (payment_error_diff * len(payment_errors) +
                       error_case_diff * len(error_cases)) / (len(payment_errors) + len(error_cases))

    projected_monthly_impact = projected_error_cases * avg_error_impact
    projected_annual_impact = projected_monthly_impact * 12

    print(f"\nAssumptions:")
    print(f"  MS SNAP households (est.): {ms_snap_households:,}")
    print(f"  Sample error rate: {100*sample_error_rate:.1f}%")
    print(f"  Average error impact: ${avg_error_impact:.2f}/case/month")

    print(f"\nProjected Impact:")
    print(f"  Error cases statewide: {projected_error_cases:,.0f}")
    print(f"  Monthly impact: ${projected_monthly_impact:,.0f}")
    print(f"  Annual impact: ${projected_annual_impact:,.0f}")

    # Error types and patterns
    print("\n" + "=" * 80)
    print("ERROR PATTERNS AND INSIGHTS")
    print("=" * 80)

    print("\nKey Findings:")
    print(f"1. Error Rate: {100*sample_error_rate:.1f}% of cases have some type of error")
    print(f"2. Payment errors ({100*len(payment_errors)/len(ms_df):.1f}% of cases):")
    print(f"   - Still receiving benefits but wrong amount")
    print(f"   - Average impact: ${payment_error_diff:+.2f} per case")

    print(f"3. Error cases ({100*len(error_cases)/len(ms_df):.1f}% of cases):")
    print(f"   - Should not be receiving benefits OR major calculation errors")
    print(f"   - Average impact: ${error_case_diff:+.2f} per case")

    # Distribution of error amounts
    print("\n" + "=" * 80)
    print("DISTRIBUTION OF BENEFIT AMOUNTS BY ERROR TYPE")
    print("=" * 80)

    # Create benefit amount bins
    bins = [0, 100, 200, 300, 400, 500, 1000, 5000]
    labels = ['$0-100', '$100-200', '$200-300', '$300-400', '$400-500', '$500-1000', '$1000+']

    for name, subset in [("Correct Cases", correct_cases),
                          ("Payment Errors", payment_errors),
                          ("Error Cases", error_cases)]:
        print(f"\n{name}:")
        subset['benefit_bin'] = pd.cut(subset['FSBEN'], bins=bins, labels=labels)
        for label in labels:
            count = len(subset[subset['benefit_bin'] == label])
            pct = 100 * count / len(subset) if len(subset) > 0 else 0
            print(f"  {label}: {count:3d} cases ({pct:5.1f}%)")

    return ms_df, correct_cases, payment_errors, error_cases

if __name__ == "__main__":
    ms_df, correct, payment_err, error = analyze_error_impact()
