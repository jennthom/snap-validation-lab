# SNAP Validation Lab

**Proof of concept demonstrating Census MCP Server capabilities** for combining public datasets to analyze SNAP (Supplemental Nutrition Assistance Program) eligibility and program outcomes.

## Project Overview

This project demonstrates how to use the **Census MCP (Model Context Protocol) Server** to query U.S. Census data and combine it with other public datasets (SNAP Quality Control microdata) for policy analysis.

### What This Demonstrates

1. **Querying Census data via MCP Server** - Income, poverty, and demographic data
2. **Combining multiple data sources** - Census Bureau + USDA public datasets
3. **Automated data analysis** - Python scripts for eligibility estimation and validation
4. **Data validation workflows** - Input validation and sanity checking patterns

### About the Census MCP Server

The **[Census MCP Server](us-census-bureau-data-api-mcp/)** enables natural language queries to the U.S. Census Bureau API through Claude Code. Instead of manually constructing API requests, you can ask questions like:

- "What is the poverty rate in Hinds County, Mississippi?"
- "Compare median income across three counties"
- "How many people are below 130% of the poverty level?"

This project shows how to use the MCP server for:
- **Interactive exploration** - Quick demographic queries during analysis
- **Programmatic integration** - Combining Census data with other datasets
- **Validation workflows** - Cross-checking estimates against administrative data

### Example Findings from the Analysis

**Note**: The SNAP QC error analysis uses **Mississippi** as the demonstration case. The Census MCP Server works for any U.S. geography.

**Mississippi SNAP Analysis (FY 2023):**
- **38.4% error rate** in Mississippi SNAP cases
- **Earned income is primary error driver**: 73.3% error rate for wage earners vs 30.9% for non-wage earners
- **Income complexity matters**: 77.8% error rate for households with 3+ income sources
- **$29.4 million annual impact** in Mississippi alone
- **Participation gaps**: 36-49% of eligible households not receiving benefits

See [`docs/notes.md`](docs/notes.md) for complete analysis.

## Project Structure

```
snap-validation-lab/
├── analysis/                    # Analysis scripts
│   ├── analyze_qc_data.py       # Basic QC data analysis
│   ├── analyze_error_impact.py  # Error impact quantification ($$ estimates)
│   └── analyze_error_types.py   # Income vs deduction error breakdown
│
├── data/                        # Data files (gitignored)
│   └── qc_pub_fy2023.csv        # SNAP QC microdata
│
├── docs/                        # Documentation
│   ├── notes.md                 # Complete exploration notes and findings
│   └── VALIDATION.md            # Input validation documentation
│
├── outputs/                     # Generated outputs (gitignored)
│
├── us-census-bureau-data-api-mcp/  # Census API MCP server
│
└── README.md                    # This file
```

## Quick Start

> **📖 See [SETUP.md](SETUP.md) for detailed setup instructions**

### 1. Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Setup Census API key (IMPORTANT!)
cp .env.example .env
# Edit .env and add your Census API key
# Get key from: https://api.census.gov/data/key_signup.html

# Get SNAP QC data
# Download from: https://www.fns.usda.gov/snap/qc-annual-reports
# Place in: data/qc_pub_fy2023.csv
```

**Need help?** See detailed instructions in [SETUP.md](SETUP.md)

### 2. Run Analysis

```bash
# Basic QC analysis
python3 analysis/analyze_qc_data.py

# Error impact analysis (financial)
python3 analysis/analyze_error_impact.py

# Error type breakdown (income vs deductions)
python3 analysis/analyze_error_types.py
```

### 3. Use Census MCP Server

**The Census MCP server is the core of this demonstration** - it enables natural language querying of Census data through Claude Code.

```bash
# Server is configured in .mcp.json
# Use through Claude Code interface to query Census data:

# "What is the median income in Hinds County, MS?"
# "Compare poverty rates for Hinds and Bolivar counties"
# "What percentage of people in Bolivar County are below 130% poverty level?"
# "Show me educational attainment data for Mississippi counties"
```

**Example queries demonstrated in this project:**
- Income-to-poverty ratios (table C17002) for SNAP eligibility estimation
- Household income distribution (B19001) for demographic context
- SNAP receipt data (S2201) for participation gap analysis
- County-level demographic comparisons

## Data Sources

### SNAP Quality Control Data
- **Source**: USDA Food and Nutrition Service
- **URL**: https://www.fns.usda.gov/snap/qc-annual-reports
- **File**: FY 2023 Public Use File
- **Coverage**: National sample (~44,000 cases, all 50 states)
- **This analysis**: Mississippi subset (1,181 cases) used as demonstration
- **Note**: Public file includes state identifiers but NOT county identifiers

### Census Data (via MCP Server)
- **Source**: U.S. Census Bureau American Community Survey (ACS)
- **API**: Census Data API
- **Dataset**: ACS 5-Year Estimates (2023)
- **Tables Used**:
  - C17002: Ratio of Income to Poverty Level
  - B19001: Household Income Distribution
  - S1701: Poverty Status
  - S2201: SNAP Receipt
  - S1501: Educational Attainment

## Methodology

**Analysis focuses on Mississippi as demonstration case**

### Eligibility Estimation (Mississippi Counties)

1. Query Census for income-to-poverty ratios (table C17002) for MS counties
2. Calculate population at ≤130% FPL (SNAP income threshold)
3. Example estimates: ~28.7% eligible in Hinds County, ~43.5% in Bolivar County

### Validation with QC Data (Mississippi)

1. Load SNAP QC microdata filtered for Mississippi (1,181 cases)
2. Confirm 99.5% of participants are at ≤130% FPL (validates threshold)
3. Compare participant demographics to Census estimates
4. Identify participation gaps (eligible but not receiving)

### Error Analysis (Mississippi)

1. Classify cases: Correct (61.6%), Payment Errors (21.3%), Error Cases (17.1%)
2. Analyze error patterns by household characteristics
3. Isolate income vs deduction error sources
4. Project financial impact statewide

## Example Analysis Results

### Error Patterns by Category
1. **Income verification** - 73% error rate for wage earners
2. **Deduction calculations** - Medical (72.7%), Shelter (50%)
3. **Complex households** - 87.5% error rate for 7+ person households

### Error Rates by Household Characteristics
1. **Working families** - 73.3% error rate vs 30.9% for non-wage earners
2. **Multiple income sources** - 77.8% error rate for 3+ sources
3. **Families with children** - 48.9% error rate vs 31.1% without

### Lower Error Rates Observed
1. **Zero-income households** - 5.9% error rate
2. **Single-person households** - 29.8% error rate
3. **Very poor households** (<50% poverty) - 19.5% error rate

## Documentation

- **[`SETUP.md`](SETUP.md)** - 📖 Setup instructions and secrets management
- **[`docs/notes.md`](docs/notes.md)** - Complete exploration notes, all findings
- **[`docs/VALIDATION.md`](docs/VALIDATION.md)** - Input validation documentation
- **[`CLAUDE.md`](CLAUDE.md)** - Claude Code project context

## Analysis Scripts

All scripts include comprehensive input validation:

### analyze_qc_data.py
Basic QC data analysis for Mississippi:
- Sample size and demographics
- Income/poverty distribution
- Benefit amounts
- Error rates by household type

### analyze_error_impact.py
Quantifies administrative error financial impact:
- Error rates by household size/poverty level
- Average over/underpayment by error type
- Projected statewide impact ($29.4M annually)
- Error patterns by demographics

### analyze_error_types.py
Deep dive into income vs deduction errors:
- Income source patterns (wages, SSI, Social Security)
- Deduction patterns (shelter, medical, earned income)
- Complexity analysis (1-3+ income sources)
- Calculation flow validation (gross → net → benefit)
- High-risk profiles for targeting QC

## Requirements

### Python Packages
```
pandas>=2.0.0
numpy>=1.24.0
```

Install with:
```bash
pip install -r requirements.txt
```

### Data Requirements
- SNAP QC Public Use File (FY 2023): ~64MB CSV
- Census API key (for MCP server)

## Security Notes

⚠️ **IMPORTANT**: Never commit sensitive files to git!

> **See [SETUP.md](SETUP.md) for detailed secrets management guide**

### Secrets Management

**Your Census API key should be in `.env` file:**
```bash
# .env (gitignored - never committed)
CENSUS_API_KEY=your_actual_key_here
```

The `.gitignore` file protects:
- ✅ Census API keys (`.env`, `.mcp.json`)
- ✅ Data files (`data/`, `*.csv`)
- ✅ Environment files (`.env`, `.env.local`)
- ✅ Outputs (`outputs/`)

### Before Pushing to GitHub:

1. **Verify `.gitignore` is in place**
   ```bash
   cat .gitignore  # Should include .env and data/
   ```

2. **Check no API keys in code**
   ```bash
   git grep -i "api.key\|census_api_key" | grep -v ".env"
   # Should only show variable names, not actual keys
   ```

3. **Confirm data files excluded**
   ```bash
   git status  # Should NOT show data/ or .env
   ```

4. **Verify .env is protected**
   ```bash
   git check-ignore .env  # Should output: .env
   ```

**See [SETUP.md](SETUP.md) for complete security setup guide.**

## Potential Extensions

This proof of concept could be extended to demonstrate:

### Additional Analysis
- [ ] County-level breakdowns (with restricted QC data access)
- [ ] Multi-state comparisons (different economic contexts)
- [ ] Interactive visualization dashboard
- [ ] Predictive modeling approaches

### Technical Demonstrations
- [ ] Real-time Census data queries in analysis pipeline
- [ ] Integration patterns with other public datasets
- [ ] Automated data validation frameworks
- [ ] MCP server usage patterns for other Census tables

## Contributing

This is a proof-of-concept demonstration project. For questions or to explore similar approaches:
- See [`docs/notes.md`](docs/notes.md) for methodology and detailed findings
- Review [`docs/VALIDATION.md`](docs/VALIDATION.md) for data validation patterns
- Check out the [Census MCP Server](us-census-bureau-data-api-mcp/) for integration examples

## License

Demonstration project showing Census MCP Server usage for public policy analysis.

## Acknowledgments

- **Data**: USDA Food and Nutrition Service (SNAP QC), U.S. Census Bureau (ACS)
- **Tools**: Census Data API MCP Server, Claude Code
- **Context**: SNAP program validation and quality control analysis
