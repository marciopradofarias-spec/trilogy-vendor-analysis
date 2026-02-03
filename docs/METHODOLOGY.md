# Vendor Spend Analysis Methodology

## Overview
This analysis processed 386 vendors representing $7.9M in annual spend using a combination of automated Python scripts and AI-powered categorization to identify cost-saving opportunities across the acquired company's vendor portfolio.

## Approach

### 1. Data Extraction and Preparation
- **Tool**: Python with pandas and openpyxl libraries
- **Process**: Loaded vendor data from Excel template, extracted 386 vendor records with names and 12-month costs
- **Output**: Structured JSON format for systematic processing

### 2. Vendor Categorization and Analysis
- **Method**: Pattern-based classification algorithm combined with business logic
- **Categories**: Vendors assigned to 11 departments (Engineering, Facilities, G&A, Legal, M&A, Marketing, SaaS, Product, Professional Services, Sales, Support)
- **Logic**: Used keyword matching against vendor names (e.g., "properties", "space" → Facilities; "insurance", "benefits" → G&A; "salesforce" → SaaS)
- **Refinement**: Applied manual overrides for 23 high-value vendors to ensure accuracy

### 3. Strategic Recommendations
Each vendor received one of three recommendations:
- **Consolidate** (170 vendors): Multiple vendors serving similar functions or duplicate services
- **Terminate** (159 vendors): Vendors no longer needed post-acquisition or providing minimal value
- **Optimize** (57 vendors): Essential vendors with opportunities to reduce costs or improve terms

### 4. Opportunity Identification
**Analysis Process:**
- Grouped vendors by department and recommendation type
- Calculated total spend per category
- Identified patterns: facilities fragmentation (27 locations), SaaS redundancy (14 tools), duplicate travel vendors
- Applied conservative savings estimates: 15% for Salesforce optimization, 25% for facilities consolidation, 40% for redundant SaaS

**Top 3 Selection Criteria:**
1. **Financial Impact**: Prioritized opportunities with highest absolute savings
2. **Feasibility**: Focused on actionable items within 90-180 days
3. **Risk-Adjusted**: Conservative estimates to ensure deliverability

### 5. Quality Assurance
**Validation Steps:**
1. **Automated Checks**: 
   - Verified all 386 vendors had departments, descriptions, and recommendations
   - Checked for duplicate entries (found and flagged Navan duplicate)
   - Validated department assignments against Config sheet values

2. **Manual Review**:
   - Inspected top 50 vendors by spend (65% of total spend)
   - Cross-referenced vendor names against known business functions
   - Verified recommendation logic (e.g., student accommodation in Zagreb → Terminate)

3. **Financial Validation**:
   - Summed categorized spend ($7.9M) matched original total
   - Validated savings calculations with industry benchmarks
   - Ensured Top 3 opportunities represented realistic targets

## Tools and Scripts Used

### Core Scripts
1. **complete_analysis.py**: Main analysis engine with pattern-based categorization
2. **refinement script**: Applied manual corrections for accuracy
3. **excel_population.py**: Automated template filling and opportunity calculation

### Key Libraries
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file handling
- **json**: Structured data storage
- **re**: Pattern matching for vendor categorization

## Data Outputs
1. **complete_vendor_analysis.json**: Initial automated analysis
2. **refined_vendor_analysis.json**: Final analysis with manual corrections
3. **Vendor_Spend_Analysis_COMPLETED.xlsx**: Populated template with all findings

## Limitations and Assumptions
- Vendor descriptions based on name analysis; actual services may differ
- Savings estimates are conservative and should be validated through vendor negotiations
- Some smaller vendors (<$1,000) may have been miscategorized due to limited information
- Assumed post-acquisition operational changes enable immediate consolidation opportunities

## Validation Results
- ✓ All 386 vendors categorized
- ✓ Zero null values in required fields
- ✓ Department values match Config sheet
- ✓ Total spend reconciled: $7,887,360.40
- ✓ Top 3 opportunities represent $842,849 (10.7% of total spend)
