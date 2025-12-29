# Setup Guide

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/snap-validation-lab.git
cd snap-validation-lab
```

### 2. Setup Census API Key

**Get an API key:**
1. Visit https://api.census.gov/data/key_signup.html
2. Request a free API key
3. Check your email for the key

**Configure the key (Option A - Recommended):**

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env and add your actual API key
```

Your `.env` file should look like:
```bash
CENSUS_API_KEY=your_actual_api_key_here
```

**Configure the key (Option B - Alternative):**

Edit `us-census-bureau-data-api-mcp/.mcp.json`:
```json
{
  "mcpServers": {
    "census": {
      "env": {
        "CENSUS_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

⚠️ **Warning**: If you use Option B, don't commit `.mcp.json` to git!

### 3. Get SNAP QC Data

Download the SNAP Quality Control Public Use File:

1. Visit https://www.fns.usda.gov/snap/qc-annual-reports
2. Download FY 2023 Public Use File
3. Save as `data/qc_pub_fy2023.csv`

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Analysis

**Option A: Run all analyses**
```bash
./run_analysis.sh
```

**Option B: Run individual scripts**
```bash
python3 analysis/analyze_qc_data.py
python3 analysis/analyze_error_impact.py
python3 analysis/analyze_error_types.py
```

## How Secrets Are Managed

### Priority Order (mcp-connect.sh loads API key in this order):

1. **`.env` file** (recommended) - Project root `.env` file
2. **Environment variable** - Shell `CENSUS_API_KEY` environment variable
3. **`.mcp.json` file** (fallback) - Hardcoded in config file

### Why This Approach?

✅ **Secure** - `.env` file is gitignored, never committed
✅ **Flexible** - Works with different environments
✅ **Sharable** - `.env.example` template for team members
✅ **Fallback** - Still works if you forget to create `.env`

### What's Protected by .gitignore?

- ✅ `.env` - Your actual API key
- ✅ `data/` - Large data files
- ✅ `outputs/` - Generated files
- ✅ `us-census-bureau-data-api-mcp/.mcp.json` - Can contain API key

### What Gets Committed?

- ✅ `.env.example` - Template (no real key)
- ✅ `analysis/` - Analysis scripts
- ✅ `docs/` - Documentation
- ✅ Code and configuration files (without secrets)

## Verification

### Check that secrets are protected:

```bash
# This should show .env is gitignored
git status
# Should NOT list: .env

# This should NOT show your actual API key
git grep -i "census_api_key"
# Should only show variable names, not the actual key

# Verify .gitignore is working
git check-ignore .env
# Should output: .env
```

### Test Census MCP Server:

Use Claude Code to query:
```
"What is the population of Hinds County, Mississippi?"
```

If it works, your API key is configured correctly! ✅

## Troubleshooting

### "Census API key not found"

1. Check `.env` file exists in project root
2. Check `.env` contains `CENSUS_API_KEY=your_key_here`
3. Check no extra spaces around `=`
4. Try fallback: Add key to `.mcp.json`

### "File not found: data/qc_pub_fy2023.csv"

1. Download QC data from: https://www.fns.usda.gov/snap/qc-annual-reports
2. Save in `data/` directory
3. Verify filename is exactly `qc_pub_fy2023.csv`

### Scripts can't find data file

Make sure you run scripts from project root:
```bash
# ✅ Correct
cd /path/to/snap-validation-lab
python3 analysis/analyze_qc_data.py

# ❌ Wrong
cd /path/to/snap-validation-lab/analysis
python3 analyze_qc_data.py
```

## Next Steps

1. ✅ Setup complete? See [README.md](README.md) for overview
2. 📚 Learn about findings? See [docs/notes.md](docs/notes.md)
3. 🔧 Understand validation? See [docs/VALIDATION.md](docs/VALIDATION.md)
4. 🚀 Ready to push to GitHub? Follow security checklist in README.md
