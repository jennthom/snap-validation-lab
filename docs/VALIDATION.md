# Input Validation Documentation

This document describes the validation checks added to all SNAP QC analysis scripts.

## Overview

All three analysis scripts now include comprehensive input validation and sanity checks to catch data quality issues early and ensure reliable results.

## Scripts Updated

1. `analyze_qc_data.py` - Basic QC data analysis
2. `analyze_error_impact.py` - Error impact quantification
3. `analyze_error_types.py` - Income vs deduction error analysis

---

## analyze_qc_data.py

### Input Validation

**File Existence:**
- Checks that `qc_pub_fy2023.csv` exists
- Provides download link if missing

**Required Columns:**
- `STATENAME` - State name
- `STATE` - State FIPS code
- `RAWHSIZE` - Household size
- `TPOV` - Income to poverty ratio
- `FSBEN` - SNAP benefit amount
- `STATUS` - Case status (1=Correct, 2=Payment Error, 3=Error Case)

**Data Availability:**
- Confirms Mississippi data exists
- Warns if < 100 cases found (expected: 1000+)

**Data Range Validation:**
- Household size: 1-20 persons (catches data entry errors)
- Poverty ratio: 0-1000% (catches coding issues)
- Benefit amount: >= $0 (catches negative values)
- STATUS: Must be 1, 2, or 3 only

### Sanity Checks

**Status Distribution:**
- Verifies all cases classified (sum = total)
- Checks percentages sum to 100%

**Poverty Bins:**
- Verifies poverty bins cover all cases
- Allows <1% gap for edge cases

---

## analyze_error_impact.py

### Input Validation

**File Existence:**
- Checks that `qc_pub_fy2023.csv` exists

**Required Columns:**
- All columns from analyze_qc_data.py PLUS:
- `FSELDER` - Has elderly members
- `FSDIS` - Has disabled members
- `FSKID` - Has children

**STATUS Validation:**
- Confirms only valid values (1, 2, 3)
- Rejects any other codes

### Sanity Checks

**Case Classification:**
- Verifies: Correct + Payment Errors + Error Cases = Total
- Ensures no cases are double-counted or missed

**Percentage Totals:**
- Confirms error type percentages sum to 100%
- Allows <0.1% rounding tolerance

---

## analyze_error_types.py

### Input Validation

**File Existence:**
- Checks that `qc_pub_fy2023.csv` exists

**Required Columns:**
- All STATUS columns PLUS:

**Income Sources:**
- `FSWAGES` - Wage income
- `FSSLFEMP` - Self-employment income
- `FSSOCSEC` - Social Security
- `FSSSI` - SSI
- `FSCSUPRT` - Child support

**Income Totals:**
- `FSGRINC` - Gross income
- `FSNETINC` - Net income
- `FSBEN` - Benefit amount

**Deductions:**
- `FSSTDDED` - Standard deduction
- `FSERNDED` - Earned income deduction
- `FSDEPDED` - Dependent care deduction
- `FSMEDDED` - Medical deduction
- `SHELDED` - Shelter deduction
- `FSTOTDED` - Total deductions

**Data Type Validation:**
- Confirms numeric columns are actually numeric
- Prevents calculation errors from string data

### Sanity Checks

**Calculation Flow:**
```
Gross Income - Deductions = Net Income
```

- Validates this relationship holds (within $5 for rounding)
- Warns if >10% of cases have discrepancies
- Indicates possible data quality issues or complex deduction rules

---

## How Validation Helps

### 1. **Catches File Issues Early**
Instead of: "KeyError: 'STATENAME'" halfway through analysis
You get: "Required input file not found: qc_pub_fy2023.csv"

### 2. **Validates Data Structure**
Instead of: Silent failures or wrong results
You get: "Missing required columns: ['FSBEN', 'STATUS']"

### 3. **Detects Data Quality Problems**
Instead of: Incorrect percentages or impossible values
You get: "WARNING: Only 50 MS cases found. Expected 1000+."

### 4. **Ensures Calculation Integrity**
Instead of: Percentages summing to 103%
You get: "Assertion Error: Percentages don't sum to 100%: 103.2%"

---

## Running the Scripts

All scripts now provide clear error messages if validation fails:

```bash
python3 analyze_qc_data.py
# If successful: Runs analysis and prints results
# If fails: Shows specific error with helpful message

python3 analyze_error_impact.py
# Validates additional demographic columns

python3 analyze_error_types.py
# Validates full income/deduction structure
```

## When Validation Might Fail

### Expected Failures:

1. **File not found** - Download QC data first
2. **Wrong file format** - Using wrong year or data source
3. **Missing columns** - File corrupted or wrong structure
4. **No state data** - State name misspelled or not in dataset

### Unexpected Failures:

If validation fails unexpectedly:
1. Check file is complete (not truncated)
2. Verify it's the public QC file (not restricted version)
3. Confirm it's FY 2023 data
4. Check for corruption during download

---

## Maintenance

When updating for new QC data years:
1. Column names may change - update `required_columns` lists
2. STATUS codes may change - update valid values
3. Expected case counts may change - update thresholds
4. New variables may be added - add to validation if used

## Questions?

See `notes.md` for analysis methodology and findings.
