#!/usr/bin/env python3
"""
Vendor Spend Analysis Tool
Uses Claude API to categorize vendors, generate descriptions, and provide strategic recommendations.
"""

import pandas as pd
import json
import os
import time
from anthropic import Anthropic
from typing import Dict, List

# Configuration
BATCH_SIZE = 20  # Process vendors in batches
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# Valid departments from Config sheet
VALID_DEPARTMENTS = [
    "Engineering", "Facilities", "G&A", "Legal", "M&A",
    "Marketing", "SaaS", "Product", "Professional Services", 
    "Sales", "Support"
]

def load_vendors(file_path: str) -> pd.DataFrame:
    """Load vendor data from Excel file."""
    df = pd.read_excel(file_path, sheet_name='Vendor Analysis Assessment')
    print(f"Loaded {len(df)} vendors")
    return df

def analyze_vendor_batch(client: Anthropic, vendors: List[Dict]) -> List[Dict]:
    """
    Analyze a batch of vendors using Claude API.
    Returns structured data: department, description, recommendation.
    """
    vendor_list = "\n".join([
        f"{i+1}. {v['Vendor Name']} - ${v['Last 12 months Cost (USD)']:,.2f}"
        for i, v in enumerate(vendors)
    ])
    
    prompt = f"""You are analyzing vendor spend for a software company acquisition. For each vendor below, provide:

1. **Department**: Assign to ONE of these departments:
   {', '.join(VALID_DEPARTMENTS)}

2. **Description**: A concise one-line description (max 15 words) of what the vendor does.

3. **Recommendation**: Choose ONE action:
   - "Terminate" - Vendor is no longer needed
   - "Consolidate" - Multiple vendors serve similar functions
   - "Optimize" - Useful but opportunity to reduce cost/usage

Guidelines:
- Be specific and actionable
- Consider the annual spend when recommending
- Look for duplicate/overlapping services for consolidation opportunities
- Focus on business impact, not just cost cutting

Vendors to analyze:
{vendor_list}

Respond ONLY with a valid JSON array (no markdown, no explanation):
[
  {{
    "vendor_name": "Vendor Name",
    "department": "Department",
    "description": "One-line description",
    "recommendation": "Terminate|Consolidate|Optimize"
  }}
]
"""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract JSON from response
        content = response.content[0].text.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        results = json.loads(content.strip())
        return results
        
    except Exception as e:
        print(f"Error analyzing batch: {e}")
        print(f"Response content: {content if 'content' in locals() else 'No response'}")
        return []

def process_all_vendors(df: pd.DataFrame, api_key: str) -> pd.DataFrame:
    """Process all vendors in batches."""
    client = Anthropic(api_key=api_key)
    
    # Prepare vendor data
    vendors = df[['Vendor Name', 'Last 12 months Cost (USD)']].to_dict('records')
    
    all_results = []
    total_batches = (len(vendors) + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\nProcessing {len(vendors)} vendors in {total_batches} batches...")
    
    for i in range(0, len(vendors), BATCH_SIZE):
        batch = vendors[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        
        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} vendors)...", end=" ")
        
        results = analyze_vendor_batch(client, batch)
        all_results.extend(results)
        
        print(f"✓ ({len(all_results)} total)")
        
        # Rate limiting
        if i + BATCH_SIZE < len(vendors):
            time.sleep(1)
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Merge with original data
    df_merged = df.merge(
        results_df,
        left_on='Vendor Name',
        right_on='vendor_name',
        how='left'
    )
    
    # Update columns
    df_merged['Department'] = df_merged['department']
    df_merged['1-line Description on what the Vendor does'] = df_merged['description']
    df_merged['Suggestions (Consolidate / Terminate / Optimize costs)'] = df_merged['recommendation']
    
    # Drop temporary columns
    df_merged = df_merged.drop(columns=['vendor_name', 'department', 'description', 'recommendation'], errors='ignore')
    
    return df_merged

def main():
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please run: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Load data
    input_file = "Copy of A - TEMPLATE - RWA - Vendor Spend Strategy (NAME).xlsx"
    df = load_vendors(input_file)
    
    # Process vendors
    df_analyzed = process_all_vendors(df, api_key)
    
    # Save intermediate results
    df_analyzed.to_csv('vendors_analyzed.csv', index=False)
    print(f"\n✓ Saved analyzed data to vendors_analyzed.csv")
    
    # Show summary
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nTotal vendors analyzed: {len(df_analyzed)}")
    print(f"\nDepartment breakdown:")
    print(df_analyzed['Department'].value_counts())
    print(f"\nRecommendation breakdown:")
    print(df_analyzed['Suggestions (Consolidate / Terminate / Optimize costs)'].value_counts())
    
    return df_analyzed

if __name__ == "__main__":
    main()
