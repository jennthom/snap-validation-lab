# Notes

# Census MCP + SNAP QC Exploration

## Setup (Day 1-2)
- What I tried
- What worked/failed
Path issues with the census API key
direct API calls work but MCP API calls do not
still messing with the configuration, have it now both running in Claude Code and Claude Desktop
fetch-aggregate-data still not working very well

✅ Success! The fix worked!

  The MCP server is now returning proper JSON responses instead of HTML. The manual test confirmed that list-datasets is working correctly and returning the full list of Census datasets as JSON.

  What was fixed:

  1. ✅ Removed console.log from DatabaseService initialization
  2. ✅ Removed console.log from fetch-aggregate-data.tool.ts
  3. ✅ Removed all console.log/error calls from fetch-dataset-geography.tool.ts
  4. ✅ Added DEBUG_LOGS environment variable to .mcp.json
  5. ✅ Rebuilt and restarted the Docker container
  6. ✅ Verified the fix with successful JSON response



- Questions

## Queries & Results (Day 3)

 Here's the income distribution comparison for Hinds County and Bolivar County, Mississippi (2023 ACS 5-year estimates):

  Total Households:
  - Hinds County: 89,720 households
  - Bolivar County: 11,907 households

  Income Distribution by Bracket:

  | Income Range        | Hinds County | %     | Bolivar County | %     |
  |---------------------|--------------|-------|----------------|-------|
  | Less than $10,000   | 7,059        | 7.9%  | 1,465          | 12.3% |
  | $10,000 - $14,999   | 5,808        | 6.5%  | 1,383          | 11.6% |
  | $15,000 - $19,999   | 4,470        | 5.0%  | 812            | 6.8%  |
  | $20,000 - $24,999   | 5,288        | 5.9%  | 715            | 6.0%  |
  | $25,000 - $29,999   | 4,441        | 5.0%  | 693            | 5.8%  |
  | $30,000 - $34,999   | 5,012        | 5.6%  | 642            | 5.4%  |
  | $35,000 - $39,999   | 3,828        | 4.3%  | 560            | 4.7%  |
  | $40,000 - $44,999   | 4,807        | 5.4%  | 370            | 3.1%  |
  | $45,000 - $49,999   | 4,177        | 4.7%  | 580            | 4.9%  |
  | $50,000 - $59,999   | 6,213        | 6.9%  | 794            | 6.7%  |
  | $60,000 - $74,999   | 9,023        | 10.1% | 962            | 8.1%  |
  | $75,000 - $99,999   | 11,542       | 12.9% | 1,007          | 8.5%  |
  | $100,000 - $124,999 | 5,644        | 6.3%  | 730            | 6.1%  |
  | $125,000 - $149,999 | 4,099        | 4.6%  | 308            | 2.6%  |
  | $150,000 - $199,999 | 4,287        | 4.8%  | 330            | 2.8%  |
  | $200,000 or more    | 4,022        | 4.5%  | 556            | 4.7%  |

  Key Findings:
  - Bolivar County has a higher concentration of low-income households: 23.9% earn less than $15,000 compared to 14.4% in Hinds County
  - Hinds County has more households in the middle-upper income ranges ($60k-$150k): 33.9% vs 25.3% in Bolivar County
  - Both counties have similar percentages earning $200k+ (4.5% vs 4.7%)
  - Bolivar County appears to have higher poverty rates with nearly 1 in 4 households earning less than $15,000 annually

  Poverty Rates (Population Below Poverty Level):
  - Bolivar County: 33.7% (highest)
  - Hinds County: 21.6%

  Key Findings:
  - Bolivar County's poverty rate is 12.1 percentage points higher than Hinds County
  - 1 in 3 people in Bolivar County live below the poverty level
  - 1 in 5 people in Hinds County live below the poverty level

  This aligns with the income distribution data we saw earlier:
  - Bolivar County had 23.9% of households earning less than $15,000
  - Hinds County had 14.4% of households earning less than $15,000

  Bolivar County faces significantly more severe economic challenges, with a poverty rate that's more than 50% higher than Hinds County's rate.

### SNAP Analysis

**SNAP Receipt Rates (Households Currently Receiving Benefits):**
- Bolivar County: 27.9%
- Hinds County: 14.7%

**Calculating SNAP Eligibility at 130% FPL:**

Using Census table C17002 (Ratio of Income to Poverty Level):

Hinds County (Population: 213,701):
- Under 50% FPL: 21,131
- 50-99% FPL: 25,070
- 100-124% FPL: 12,444
- 125-149% FPL: 13,213

Bolivar County (Population: 27,895):
- Under 50% FPL: 4,522
- 50-99% FPL: 4,882
- 100-124% FPL: 2,421
- 125-149% FPL: 1,620

**Estimated SNAP-Eligible Population (130% FPL):**
- Hinds County: 61,287 people (28.7% of population)
- Bolivar County: 12,149 people (43.5% of population)

**SNAP Participation Analysis:**

| County | Poverty Rate | Est. SNAP Eligible (130% FPL) | SNAP Receipt | Participation Gap |
|--------|--------------|-------------------------------|--------------|-------------------|
| Hinds | 21.6% | 28.7% | 14.7% | 14.0 points |
| Bolivar | 33.7% | 43.5% | 27.9% | 15.6 points |

**Key Insights:**
- About 14-16 percentage points of potentially eligible people in both counties are NOT receiving SNAP benefits
- Bolivar County has higher estimated eligibility (43.5%) but similar participation gap
- Both counties show significant under-enrollment in SNAP relative to estimated eligibility
- In Bolivar County, about 64% of eligible population receives SNAP (27.9% / 43.5%)
- In Hinds County, about 51% of eligible population receives SNAP (14.7% / 28.7%)

**Methodology Notes:**
- Eligibility calculated as sum of: under 50% + 50-99% + 100-124% + (20% of 125-149% bracket)
- 130% FPL falls at approximately 20% mark of the 125-149% bracket
- This is income-based eligibility only; actual SNAP eligibility also considers assets, work requirements, and household composition







...

## Integration with QC data (Day 3-4)

### SNAP QC Microdata Analysis (FY 2023)

**Data Source:** qc_pub_fy2023.csv - SNAP Quality Control microdata

**Mississippi Sample:**
- 1,181 household cases
- Average household size: 2.10 persons
- Total persons in sample: 2,486

**Income to Poverty Ratio Distribution:**
| Poverty Level | Count | Percentage |
|---------------|-------|------------|
| Below 50% poverty | 487 | 41.2% |
| 50-100% poverty | 541 | 45.8% |
| 100-130% poverty (SNAP eligible) | 147 | 12.4% |
| Above 130% poverty | 6 | 0.5% |

**Key Finding:** 99.5% of SNAP participants are at or below 130% FPL (as expected)

**SNAP Benefit Amounts:**
- Average monthly benefit: $349.94
- Median monthly benefit: $281.00
- Total monthly benefits (sample): $413,275

**Household Composition:**
| Size | Count | Percentage |
|------|-------|------------|
| 1 person | 635 | 53.8% |
| 2 persons | 179 | 15.2% |
| 3 persons | 145 | 12.3% |
| 4 persons | 114 | 9.7% |
| 5+ persons | 108 | 9.1% |

**Quality Control Findings (Error Rates):**
| Status | Count | Percentage |
|--------|-------|------------|
| Active - Correct | 727 | 61.6% |
| Active - Payment Error | 252 | 21.3% |
| Error Case | 202 | 17.1% |

**Overall error rate: 38.4%**

**Demographic Characteristics:**
- Households with elderly: 302 (25.6%)
- Households with disabled: 288 (24.4%)
- Households with children: 489 (41.4%)

### Cross-Validation: Census vs QC Data

**Census Estimates (130% FPL eligibility):**
- Hinds County: 28.7% of population eligible
- Bolivar County: 43.5% of population eligible

**QC Data Shows:**
- 99.5% of actual participants are at/below 130% FPL
- 38.4% error rate in benefit administration
- Predominantly single-person households (53.8%)
- High poverty concentration: 87% below 100% FPL

**Participation Gap Analysis:**
Using Census estimates and SNAP receipt data:
- Hinds: ~51% of eligible population participates
- Bolivar: ~64% of eligible population participates

**Key Insights for Validation:**
1. QC microdata confirms Census eligibility calculations are directionally correct
2. Error rates suggest 38% of cases have payment or eligibility issues
3. Single-person households dominate SNAP participation (54% vs ~26% of general population)
4. Very high poverty concentration among participants (87% below poverty line vs 21-34% poverty rate in counties)
5. Significant non-participation among eligible households (36-49% eligible but not receiving benefits)

**What This Enables:**
- Validate demographic composition of eligible population
- Estimate true participation rates vs eligible population
- Identify characteristics of non-participating eligible households
- Quantify administrative error impact on benefit accuracy
- Model expected benefit amounts for newly eligible households

### Detailed Error Type Analysis: Income vs Deductions

**Analysis Source:** analyze_error_types.py

#### 🚨 CRITICAL FINDING: Earned Income is the Primary Error Driver

**Error Rates by Income Complexity:**
| Number of Income Sources | Error Rate | Cases |
|-------------------------|------------|-------|
| 0 sources (no income) | 5.9% ✅ | 323 |
| 1 source | 45.0% | 615 |
| 2 sources | 64.0% | 225 |
| 3 sources | 77.8% ⚠️ | 18 |

**Error Rates by Income Type:**
- **Cases with wages: 73.3% error rate**
- Cases without wages: 30.9% error rate
- **Impact: +42.4 percentage points**

**Deduction Complexity Issues:**
- Medical deductions claimed: 72.7% error rate (vs 36.0% without)
- Shelter deductions claimed: 50.0% error rate (vs 26.3% without)
- Earned income deduction: Strong association with errors

**Highest Risk Profile:**
- **Complex cases** (2+ income sources AND above-median deductions): **77.7% error rate**
- **Simple cases** (0-1 income sources AND below-median deductions): **20.4% error rate**
- **Risk difference: +57.3 percentage points**

#### The Income Paradox

**Benefit Calculation Flow Analysis:**

| Case Type | Avg Gross Income | Avg Deductions | Avg Net Income | Avg Benefit |
|-----------|------------------|----------------|----------------|-------------|
| Correct Cases | $574 | $336 | $309 | $343 |
| Payment Errors | $1,286 | $493 | $890 | $319 |
| Error Cases | $1,098 | $522 | $648 | $412 |

**Key Paradox:** Error cases have:
- **91% higher gross income** than correct cases ($1,098 vs $574)
- **20% higher benefits** than correct cases ($412 vs $343)
- Should receive LOWER benefits but receive MORE

**Zero Income Cases:**
- Correct cases: 36% have $0 gross income (very simple)
- Payment errors: 0.8% have $0 income
- Error cases: 5% have $0 income

#### Income Source Patterns by Error Type

**Wage Income (FSWAGES):**
- Correct cases: 7.7% have wages (avg $1,178)
- Payment errors: 35.3% have wages (avg $1,604)
- Error cases: 32.2% have wages (avg $1,285)

**Social Security (FSSOCSEC):**
- Correct cases: 26.7% receive (avg $933)
- Payment errors: 40.9% receive (avg $880)
- Error cases: 33.2% receive (avg $952)

**SSI (FSSSI):**
- Correct cases: 25.4% receive (avg $671)
- Payment errors: 37.7% receive (avg $659)
- Error cases: 34.2% receive (avg $702)

**Child Support (FSCSUPRT):**
- Correct cases: 7.4% receive (avg $321)
- Payment errors: 19.0% receive (avg $302)
- Error cases: 23.3% receive (avg $288)

#### Financial Impact by Error Type

**From Previous Analysis:**
- Total sample: 1,181 cases
- Correct cases: 727 (61.6%)
- Payment errors: 252 (21.3%) - UNDERPAID by $24.16/month avg
- Error cases: 202 (17.1%) - OVERPAID by $68.89/month avg

**Projected Statewide (Mississippi):**
- Error cases: ~141,851
- Monthly impact: $2.4 million
- **Annual impact: $29.4 million**

**Error Rate by Household Size:**
| Size | Error Rate |
|------|------------|
| 1 person | 29.8% |
| 2 persons | 39.7% |
| 3 persons | 44.1% |
| 4 persons | 54.4% |
| 5 persons | 56.2% |
| 6 persons | 67.7% |
| 7 persons | 87.5% |
| 8 persons | 80.0% |

#### Root Causes Identified

**1. Income Verification Failures**
- Error cases have nearly 2× income but higher benefits
- Suggests unreported/underreported wages
- Income verification processes failing for working poor

**2. Wage Complexity**
- 73% error rate for wage earners
- Fluctuating monthly income hard to track
- Multiple jobs complicate reporting
- Earned income deduction calculation adds complexity

**3. Deduction Calculation Errors**
- Medical expenses: highly error-prone (72.7% error rate)
- Shelter costs: complex calculations (50% error rate)
- Interaction between deductions and income creates compounding errors

**4. Payment Errors vs Error Cases (Different Problems)**
- **Payment errors**: Eligible people receiving wrong amount (mostly underpaid)
  - Highest gross income ($1,286)
  - Lowest benefits ($319)
  - Appear to be legitimate calculation errors
- **Error cases**: Ineligible people receiving benefits (overpaid)
  - High gross income ($1,098)
  - Highest benefits ($412)
  - Should not be receiving benefits at all

**5. System Handles Simple Cases Well**
- No income + few deductions = 5.9% error rate
- Deepest poverty cases processed correctly
- Errors concentrate at 50-130% poverty (working poor with fluctuating income)

#### Implications for Validation Work

**Where Errors Occur:**
1. **Income verification** (73% error rate for wage earners)
2. **Deduction calculations** (medical 72.7%, shelter 50%)
3. **Complex household compositions** (87.5% error rate for 7+ person households)

**Who Gets Hurt:**
1. **Working poor families** with fluctuating wages (underpaid)
2. **Complex households** with multiple income sources
3. **Families with children** (48.9% error rate vs 31.1% without)

**System Strengths:**
1. **Zero-income households** handled well (5.9% error rate)
2. **Single-person households** more accurate (29.8% error rate)
3. **Very poor households** (<50% poverty) have lowest error rates (19.5%)

## Synthesis (Day 5)




## Week plan with SNAP QC integration
## Day 1-2: Census MCP exploration

Set up Census MCP, test basic queries
Get income distributions for Hinds & Bolivar counties
Calculate rough eligibility estimates using poverty thresholds
Document what works/breaks

## Day 3-4: SNAP QC data integration

Find what QC data you can access for MS (check FNS website, state reports, or your existing partnerships)
If you have microdata: great. If not: county-level aggregates work fine for this
Pull actual participation numbers for your test counties
Build comparison: Census-estimated eligible vs QC actual participants

## Day 5: Analysis + synthesis

Calculate participation rates, demographic gaps
Test whether this pattern could validate your team's models
Write up what you learned (for yourself, maybe for team hack session)

Bonus if time:

Try PA for comparison (different economic context)
Think through: "Could this become production evaluation infrastructure?"
Prototype simple dashboard or report
