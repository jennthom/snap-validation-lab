# SNAP Validation Lab - Claude Code Context

## Project Purpose

**Proof of concept** demonstrating U.S. Census MCP Server capabilities for public policy analysis.

This is a **technical demonstration**, not a production policy tool. The primary goal is to showcase how the Census MCP Server enables natural language queries of Census data and integration with other public datasets.

## Key Architecture

### Census MCP Server (Core Component)
- Natural language queries for demographic data through Claude Code
- Enables queries like: "What is the poverty rate in Hinds County, MS?"
- Eliminates need to manually construct Census API requests
- Key tables used: C17002 (poverty ratios), B19001 (income), S2201 (SNAP receipt)

### SNAP QC Data Integration
- USDA Food and Nutrition Service public use file (FY 2023)
- National dataset (~44,000 cases, all 50 states)
- **This analysis uses Mississippi as demonstration** (1,181 cases)
- Census MCP Server works for any U.S. state/county
- Demonstrates combining Census data with other public datasets

### Analysis Scripts
- Python/pandas-based analysis
- Input validation patterns documented in `docs/VALIDATION.md`
- All scripts work from project root directory

## Important Conventions

### File Paths
All Python scripts use relative paths from project root:
```python
input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'qc_pub_fy2023.csv')
```

Never use hard-coded paths. Scripts must work regardless of current working directory.

### Secrets Management
- Census API key stored in `.env` file (gitignored)
- Never commit `.env`, `data/`, or `us-census-bureau-data-api-mcp/.mcp.json`
- Use `.env.example` as template for team members
- Priority order: `.env` → environment variable → `.mcp.json`

### Analysis Patterns
- All scripts include comprehensive input validation
- Document validation checks in code comments
- Use descriptive error messages for validation failures
- See `docs/VALIDATION.md` for complete validation patterns

### Code Style
- Use pandas for data analysis
- Include clear section headers in analysis output
- Validate data integrity before calculations
- Document assumptions in comments

## Data Sources

### SNAP QC Microdata
- **Location**: `data/qc_pub_fy2023.csv` (gitignored, not in repo)
- **Source**: https://www.fns.usda.gov/snap/qc-annual-reports
- **Size**: 64MB, ~44,000 cases (all 50 states)
- **This analysis**: Filtered for Mississippi only (FIPSST = 28)
- **Coverage**: National sample with state identifiers (no county identifiers)
- **Note**: Analysis scripts can be adapted for any state

### Census Data (via MCP Server)
- **Table C17002**: Ratio of Income to Poverty Level (for SNAP eligibility estimation)
- **Table B19001**: Household Income Distribution
- **Table S1701**: Poverty Status
- **Table S2201**: SNAP Receipt
- **Table S1501**: Educational Attainment
- **Dataset**: ACS 5-Year Estimates (2023)

## Common Workflows

### Running Analysis Scripts
```bash
# Run individual scripts from project root
python3 analysis/analyze_qc_data.py
python3 analysis/analyze_error_impact.py
python3 analysis/analyze_error_types.py

# Or run all at once
./run_analysis.sh
```

### Querying Census Data via MCP Server
Use natural language through Claude Code interface:
- "What is the poverty rate in Hinds County, Mississippi?"
- "Compare median income for Hinds and Bolivar counties"
- "How many people are below 130% of the poverty level in Bolivar County?"
- "Show me SNAP participation rates by county"

### Setup for New Users
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup Census API key
cp .env.example .env
# Edit .env and add actual API key

# 3. Download SNAP QC data
# Get from: https://www.fns.usda.gov/snap/qc-annual-reports
# Place in: data/qc_pub_fy2023.csv
```

## Guidelines

### ✅ DO:
- **Emphasize proof of concept nature** - This demonstrates MCP server capabilities
- **Focus on Census MCP Server** - That's the primary technical contribution
- **Use analysis as examples** - Show what's possible with combined datasets
- **Ask before creating new files** - Especially documentation/markdown files
- **Maintain relative file paths** - Scripts must be portable
- **Validate inputs thoroughly** - Follow patterns in VALIDATION.md

### ❌ DON'T:
- **Create detailed policy recommendations** - This is a technical demo, not policy guidance
- **Present as production tool** - It's exploratory/proof-of-concept
- **Commit secrets or data** - API keys and CSV files are gitignored
- **Create intervention documents** - Too much detail for a POC
- **Hard-code file paths** - Use os.path.join with relative paths
- **Skip input validation** - All scripts should validate data integrity

### When User Asks About Interventions/Policy:
- Discuss concepts conversationally
- Don't create detailed markdown documents
- Remember: this is a technical demonstration, not policy development

## Project Structure

```
snap-validation-lab/
├── analysis/                          # Python analysis scripts
│   ├── analyze_qc_data.py             # Basic QC data analysis
│   ├── analyze_error_impact.py        # Error impact quantification
│   └── analyze_error_types.py         # Income vs deduction errors
│
├── data/                              # Data files (gitignored)
│   └── qc_pub_fy2023.csv              # SNAP QC microdata (64MB)
│
├── docs/                              # Documentation
│   ├── notes.md                       # Complete analysis findings
│   └── VALIDATION.md                  # Input validation patterns
│
├── outputs/                           # Generated outputs (gitignored)
│
├── us-census-bureau-data-api-mcp/    # Census MCP Server
│   ├── scripts/mcp-connect.sh         # Server startup script
│   └── .mcp.json                      # MCP config (gitignored)
│
├── .env                               # Census API key (gitignored)
├── .env.example                       # Template for .env
├── .gitignore                         # Protects secrets and data
├── CLAUDE.md                          # This file
├── README.md                          # Project overview
├── SETUP.md                           # Setup instructions
├── requirements.txt                   # Python dependencies
└── run_analysis.sh                    # Run all analyses
```

## Key Documentation

### README.md
- **Purpose**: Project overview with proof-of-concept emphasis
- **Audience**: GitHub visitors, potential users
- **Content**: Quick start, data sources, example findings
- **Tone**: Technical demonstration showcase

### SETUP.md
- **Purpose**: Detailed setup instructions
- **Content**: Step-by-step setup, secrets management, troubleshooting
- **Key section**: How to get and configure Census API key

### docs/notes.md
- **Purpose**: Complete analysis findings and methodology
- **Content**: Detailed exploration notes, all findings, insights
- **Audience**: Those interested in the analysis approach

### docs/VALIDATION.md
- **Purpose**: Input validation documentation
- **Content**: Required columns, data ranges, sanity checks
- **Use**: Reference when adding validation to new scripts

## Example Findings (Keep These in Mind)

**These findings are from Mississippi analysis only.** The Census MCP server works for any U.S. geography.

The analysis demonstrates the MCP server's capability to:
- Estimate SNAP eligibility using Census poverty data (C17002) - example: MS counties
- Validate estimates against administrative data (SNAP QC) - example: MS state data
- Identify error patterns (38.4% overall error rate in MS)
- Show income verification as primary error source (73.3% for wage earners in MS)
- Understand retention challenges (administrative errors cause eligible families to cycle off benefits)

These findings are **examples of what's possible**, not policy recommendations.

## Technical Capabilities Demonstrated

1. **Natural Language Census Queries** - Through MCP server
2. **Multi-Dataset Integration** - Census + USDA public data
3. **Automated Validation** - Input checking, sanity tests
4. **Error Pattern Analysis** - Statistical breakdowns by household type
5. **Financial Impact Estimation** - Projection from sample to population

## Questions & Collaboration

For questions about:
- **Methodology**: See `docs/notes.md`
- **Setup**: See `SETUP.md`
- **Validation**: See `docs/VALIDATION.md`
- **Census MCP Server**: See `us-census-bureau-data-api-mcp/README.md`

This is an exploratory demonstration project - perfect for showing what's possible with Census MCP Server integration.
