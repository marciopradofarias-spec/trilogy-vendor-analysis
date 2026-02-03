#!/usr/bin/env python3
"""
Complete Vendor Analysis Script
Processes all vendors and generates structured analysis
"""

import pandas as pd
import json
import re

def categorize_vendor(vendor_name, cost):
    """
    Categorize vendor based on name patterns and business logic.
    Returns: (department, description, recommendation)
    """
    name_lower = vendor_name.lower()
    
    # Facilities patterns
    if any(x in name_lower for x in ['properties', 'space', 'wework', 'office', 'real estate', 'facilities', 'coworking', 'property', 'tower', 'centar', 'building']):
        return ('Facilities', f'Office space and facilities provider', 'Consolidate')
    
    # Insurance patterns
    if any(x in name_lower for x in ['insurance', 'osiguranje', 'aetna', 'bupa', 'cigna', 'care health']):
        return ('G&A', f'Employee insurance and benefits provider', 'Optimize')
    
    # Legal patterns  
    if any(x in name_lower for x in ['law', 'legal', 'odvjetnicko', 'solicitors', 'attorneys']):
        return ('Legal', f'Legal services and counsel', 'Optimize')
    
    # Accounting/Finance patterns
    if any(x in name_lower for x in ['bdo', 'grant thornton', 'pwc', 'kpmg', 'deloitte', 'ey', 'rsm', 'chartered accountant', 'audit']):
        return ('Professional Services', f'Accounting, audit and financial advisory', 'Optimize')
    
    # M&A Advisory patterns
    if any(x in name_lower for x in ['houlihan', 'advisory', 'corporate finance', 'investment bank', 'capital management', 'm&a']):
        return ('M&A', f'M&A and corporate finance advisory services', 'Consolidate')
    
    # Recruitment patterns
    if any(x in name_lower for x in ['recruitment', 'recruiting', 'staffing', 'talent', 'mason frank', 'accutrainee', 'technet', 'cedar']):
        return ('G&A', f'Recruitment and staffing services', 'Consolidate')
    
    # HR/Payroll patterns
    if any(x in name_lower for x in ['hr solution', 'payroll', 'adp', 'workday', '人力', 'human resource']):
        return ('G&A', f'HR management and payroll services', 'Optimize')
    
    # Travel patterns
    if any(x in name_lower for x in ['navan', 'tripactions', 'travel', 'expedia', 'booking']):
        return ('G&A', f'Corporate travel management platform', 'Consolidate')
    
    # Telecom patterns
    if any(x in name_lower for x in ['telefonica', 'telekom', 'telecom', 'verizon', 'at&t', 'vodafone']):
        return ('G&A', f'Telecommunications and connectivity services', 'Optimize')
    
    # Cloud/AWS/Infrastructure patterns
    if any(x in name_lower for x in ['aws', 'amazon web', 'azure', 'google cloud', 'cloud hosting', 'datacentre', 'datacenter']):
        return ('Engineering', f'Cloud infrastructure and hosting services', 'Optimize')
    
    # IT Services patterns
    if any(x in name_lower for x in ['infosys', 'wipro', 'tcs', 'cognizant', 'it services', 'tech solutions', 'raunalni']):
        return ('Professional Services', f'IT consulting and professional services', 'Optimize')
    
    # Salesforce patterns (CRM)
    if 'salesforce' in name_lower:
        if cost > 1000000:
            return ('SaaS', f'Enterprise CRM platform for sales management', 'Optimize')
        else:
            return ('SaaS', f'CRM and sales automation software', 'Consolidate')
    
    # Marketing/Advertising patterns
    if any(x in name_lower for x in ['marketing', 'advertising', 'media', 'linkedin', 'google ads', 'facebook', 'hubspot', 'cognism', 'uberflip', 'mightyhive']):
        if 'linkedin' in name_lower or 'google' in name_lower:
            return ('Marketing', f'Digital advertising and lead generation platform', 'Optimize')
        else:
            return ('Marketing', f'Marketing automation and demand generation tool', 'Consolidate')
    
    # SaaS tools patterns
    if any(x in name_lower for x in ['saas', 'software', 'app', 'platform', 'kimble', 'sage', 'planful', 'workato', 'peakon', 'intralinks']):
        return ('SaaS', f'Business software and SaaS application', 'Consolidate')
    
    # Microsoft patterns
    if 'microsoft' in name_lower:
        return ('SaaS', f'Microsoft software licenses and services', 'Optimize')
    
    # Consulting patterns
    if any(x in name_lower for x in ['consulting', 'advisory', 'consultant', 'savjetovanje']):
        return ('Professional Services', f'Business consulting and advisory services', 'Optimize')
    
    # Food/Catering patterns
    if any(x in name_lower for x in ['sodexo', 'catering', 'food', 'restaurant', 'konzum']):
        return ('Facilities', f'Employee food and catering services', 'Optimize')
    
    # Benefits/Wellness patterns
    if any(x in name_lower for x in ['benefit', 'wellness', 'gym', 'fitness']):
        return ('G&A', f'Employee benefits and wellness programs', 'Optimize')
    
    # Tax patterns
    if any(x in name_lower for x in ['tax', 'porezni']):
        return ('Professional Services', f'Tax advisory and compliance services', 'Optimize')
    
    # Default categorization for unknown
    if cost > 50000:
        return ('G&A', f'Business services vendor', 'Optimize')
    elif cost < 1000:
        return ('G&A', f'Miscellaneous vendor', 'Terminate')
    else:
        return ('G&A', f'Business services vendor', 'Consolidate')

def load_and_analyze_all_vendors():
    """Load all vendors and perform complete analysis"""
    df = pd.read_excel("Copy of A - TEMPLATE - RWA - Vendor Spend Strategy (NAME).xlsx", 
                       sheet_name='Vendor Analysis Assessment')
    
    results = []
    
    print(f"Analyzing {len(df)} vendors...")
    print("-" * 80)
    
    for idx, row in df.iterrows():
        vendor_name = row['Vendor Name']
        cost = float(row['Last 12 months Cost (USD)'])
        
        dept, desc, rec = categorize_vendor(vendor_name, cost)
        
        results.append({
            'index': int(idx),
            'vendor_name': vendor_name,
            'cost': cost,
            'department': dept,
            'description': desc,
            'recommendation': rec
        })
        
        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1} vendors...")
    
    print(f"✓ Completed analysis of {len(results)} vendors")
    
    return results

def save_results(results):
    """Save results to JSON"""
    with open('complete_vendor_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved complete analysis to complete_vendor_analysis.json")

def generate_summary(results):
    """Generate analysis summary"""
    df = pd.DataFrame(results)
    
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    print(f"\nTotal vendors: {len(df)}")
    print(f"Total spend: ${df['cost'].sum():,.2f}")
    
    print(f"\n\nDepartment Distribution:")
    print(df['department'].value_counts().to_string())
    
    print(f"\n\nRecommendation Distribution:")
    print(df['recommendation'].value_counts().to_string())
    
    print(f"\n\nTop 10 Vendors by Spend:")
    top_10 = df.nlargest(10, 'cost')[['vendor_name', 'department', 'cost', 'recommendation']]
    for _, row in top_10.iterrows():
        print(f"  ${row['cost']:>12,.2f} - {row['vendor_name'][:40]:40} [{row['department']}] -> {row['recommendation']}")

if __name__ == "__main__":
    results = load_and_analyze_all_vendors()
    save_results(results)
    generate_summary(results)
