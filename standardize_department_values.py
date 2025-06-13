#!/usr/bin/env python3
"""
Department Standardization Script
Standardizes DEPARTMENT column values in the AMR dataset:
- "Out" -> "Out-patient" 
- "Inp" -> "In-patient"
- Handles case-insensitive matching
- Strips leading/trailing spaces
"""

import pandas as pd
import os
from datetime import datetime

def standardize_department_column(input_file, output_file):
    """
    Standardize DEPARTMENT column values in the dataset
    """
    print("🏥 DEPARTMENT COLUMN STANDARDIZATION")
    print("=" * 50)
    
    # Load the dataset
    print(f"📂 Loading dataset: {input_file}")
    df = pd.read_csv(input_file)
    print(f"✅ Dataset loaded successfully!")
    print(f"   📊 Shape: {df.shape}")
    
    # Check if DEPARTMENT column exists
    if 'DEPARTMENT' not in df.columns:
        print("❌ DEPARTMENT column not found in dataset!")
        print("Available columns:")
        for col in df.columns:
            print(f"   - {col}")
        return False
    
    # Analyze current DEPARTMENT values
    print(f"\n🔍 CURRENT DEPARTMENT COLUMN ANALYSIS:")
    print(f"   Records with DEPARTMENT data: {df['DEPARTMENT'].notna().sum():,}")
    print(f"   Records missing DEPARTMENT data: {df['DEPARTMENT'].isna().sum():,}")
    
    # Check for leading/trailing spaces
    if df['DEPARTMENT'].notna().any():
        values_with_spaces = df['DEPARTMENT'].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
        print(f"   Values with leading/trailing spaces: {values_with_spaces:,}")
    
    print(f"\n📋 Current DEPARTMENT values (before standardization):")
    dept_counts = df['DEPARTMENT'].value_counts(dropna=False)
    for value, count in dept_counts.items():
        percentage = (count / len(df)) * 100
        if pd.notna(value):
            print(f"   '{value}' (length: {len(str(value))}): {count:,} records ({percentage:.1f}%)")
        else:
            print(f"   Missing/NaN: {count:,} records ({percentage:.1f}%)")
    
    # Clean leading and trailing spaces
    print(f"\n🧹 CLEANING SPACES...")
    original_values_with_spaces = df['DEPARTMENT'].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
    print(f"   Values with spaces before cleaning: {original_values_with_spaces:,}")
    
    # Strip spaces and convert to string, then back to NaN where appropriate
    df['DEPARTMENT'] = df['DEPARTMENT'].astype(str).str.strip()
    df['DEPARTMENT'] = df['DEPARTMENT'].replace('nan', pd.NA)  # Convert 'nan' strings back to NaN
    
    values_with_spaces_after = df['DEPARTMENT'].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
    print(f"   Values with spaces after cleaning: {values_with_spaces_after:,}")
    
    # Create mapping dictionary (case-insensitive)
    department_mapping = {
        'Out': 'Out-patient',
        'out': 'Out-patient', 
        'OUT': 'Out-patient',
        'Inp': 'In-patient',
        'inp': 'In-patient',
        'INP': 'In-patient'
    }
    
    print(f"\n📋 DEPARTMENT MAPPING DICTIONARY:")
    unique_mappings = {}
    for code, label in department_mapping.items():
        if code.lower() not in [k.lower() for k in unique_mappings.keys()]:
            unique_mappings[code.lower()] = label
    
    for code, label in unique_mappings.items():
        print(f"   '{code}' (case-insensitive) → '{label}'")
    
    # Store original values for comparison (after space cleaning)
    original_dept_counts = df['DEPARTMENT'].value_counts(dropna=False)
    
    # Apply the mapping
    print(f"\n🔄 APPLYING STANDARDIZATION...")
    df['DEPARTMENT'] = df['DEPARTMENT'].map(department_mapping).fillna(df['DEPARTMENT'])
    
    # Check transformation results
    new_dept_counts = df['DEPARTMENT'].value_counts(dropna=False)
    
    print(f"\n📊 TRANSFORMATION RESULTS:")
    print(f"Before standardization (after space cleaning):")
    for value, count in original_dept_counts.items():
        if pd.notna(value):
            print(f"   '{value}': {count:,} records")
        else:
            print(f"   Missing/NaN: {count:,} records")
    
    print(f"\nAfter standardization:")
    for value, count in new_dept_counts.items():
        if pd.notna(value):
            print(f"   '{value}': {count:,} records")
        else:
            print(f"   Missing/NaN: {count:,} records")
    
    # Validation
    total_records = len(df)
    records_with_dept = df['DEPARTMENT'].notna().sum()
    standardized_values = df['DEPARTMENT'].isin(['Out-patient', 'In-patient']).sum()
    
    print(f"\n✅ VALIDATION RESULTS:")
    print(f"   Total records: {total_records:,}")
    print(f"   Records with DEPARTMENT data: {records_with_dept:,}")
    print(f"   Properly standardized values: {standardized_values:,}")
    
    if records_with_dept > 0:
        success_rate = (standardized_values / records_with_dept * 100)
        print(f"   Standardization success rate: {success_rate:.2f}%")
        
        # Check for any unmapped values
        unmapped_values = df[df['DEPARTMENT'].notna() & ~df['DEPARTMENT'].isin(['Out-patient', 'In-patient'])]['DEPARTMENT'].unique()
        if len(unmapped_values) > 0:
            print(f"   ⚠️  Unmapped values found: {list(unmapped_values)}")
        else:
            print(f"   ✅ All values successfully mapped!")
    else:
        print(f"   No DEPARTMENT data to standardize")
    
    # Show sample of transformed data
    print(f"\n🔍 Sample of standardized data (first 10 non-null records):")
    sample_dept = df[df['DEPARTMENT'].notna()][['ORGANISM_NAME', 'DEPARTMENT']].head(10)
    if len(sample_dept) > 0:
        for idx, row in sample_dept.iterrows():
            organism_name = str(row['ORGANISM_NAME'])[:30] if pd.notna(row['ORGANISM_NAME']) else 'Unknown'
            print(f"   {organism_name:30} | DEPT: {row['DEPARTMENT']}")
    else:
        print(f"   No records with DEPARTMENT data found for sampling")
    
    # Save the standardized dataset
    print(f"\n💾 SAVING STANDARDIZED DATASET...")
    df.to_csv(output_file, index=False)
    file_size_mb = os.path.getsize(output_file) / (1024*1024)
    
    print(f"✅ Dataset with standardized DEPARTMENT column saved!")
    print(f"   📁 Location: {output_file}")
    print(f"   📏 File size: {file_size_mb:.2f} MB")
    print(f"   📊 Records: {len(df):,}")
    print(f"   📋 Columns: {len(df.columns)}")
    
    return True

def main():
    """Main function"""
    # Input and output file paths
    input_file = r'c:\NATIONAL AMR DATA ANALYSIS FILES\data\processed\mapped\df_final_with_standardized_sex_2025-06-12_15-32-27.csv'
    output_file = r'c:\NATIONAL AMR DATA ANALYSIS FILES\Data_Department_Standardized.csv'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        print("\n📂 Available files in mapped directory:")
        mapped_dir = r'c:\NATIONAL AMR DATA ANALYSIS FILES\data\processed\mapped'
        if os.path.exists(mapped_dir):
            for file in os.listdir(mapped_dir):
                if file.endswith('.csv'):
                    print(f"   - {file}")
        return
    
    # Perform standardization
    success = standardize_department_column(input_file, output_file)
    
    if success:
        print(f"\n🎉 DEPARTMENT STANDARDIZATION COMPLETED SUCCESSFULLY!")
        print(f"📄 Final file: Data_Department_Standardized.csv")
    else:
        print(f"\n❌ Standardization failed!")

if __name__ == "__main__":
    main()
