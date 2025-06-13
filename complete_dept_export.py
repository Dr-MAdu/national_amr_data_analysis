import pandas as pd
import os

print("🚀 Completing Department Standardization Export")
print("=" * 50)

# The standardization was already performed in the notebook
# Now we need to load the latest processed data and export it

# Check for the most recent dataset with standardized sex
latest_file = r'c:\NATIONAL AMR DATA ANALYSIS FILES\data\processed\mapped\df_final_with_standardized_sex_2025-06-12_15-32-27.csv'

print(f"📂 Loading dataset: {os.path.basename(latest_file)}")
df = pd.read_csv(latest_file)

print(f"✅ Dataset loaded!")
print(f"   📊 Shape: {df.shape}")

# Apply department standardization (as performed in the notebook)
print(f"\n🏥 Applying department standardization...")

if 'DEPARTMENT' in df.columns:
    # Clean spaces
    df['DEPARTMENT'] = df['DEPARTMENT'].astype(str).str.strip()
    df['DEPARTMENT'] = df['DEPARTMENT'].replace('nan', pd.NA)
    
    # Apply mapping
    dept_mapping = {
        'Out': 'Out-patient',
        'out': 'Out-patient', 
        'OUT': 'Out-patient',
        'Inp': 'In-patient',
        'inp': 'In-patient',
        'INP': 'In-patient'
    }
    
    df['DEPARTMENT'] = df['DEPARTMENT'].map(dept_mapping).fillna(df['DEPARTMENT'])
    
    # Verify results
    dept_counts = df['DEPARTMENT'].value_counts(dropna=False)
    print(f"   📊 Department distribution after standardization:")
    for value, count in dept_counts.items():
        percentage = (count / len(df)) * 100
        if pd.notna(value):
            print(f"      '{value}': {count:,} records ({percentage:.1f}%)")
        else:
            print(f"      Missing/NaN: {count:,} records ({percentage:.1f}%)")
    
    # Export the standardized dataset
    output_file = r'c:\NATIONAL AMR DATA ANALYSIS FILES\Data_Department_Standardized.csv'
    print(f"\n💾 Exporting to: {output_file}")
    
    df.to_csv(output_file, index=False)
    file_size_mb = os.path.getsize(output_file) / (1024*1024)
    
    print(f"✅ Export completed successfully!")
    print(f"   📁 Location: {output_file}")
    print(f"   📏 File size: {file_size_mb:.2f} MB") 
    print(f"   📊 Records: {len(df):,}")
    print(f"   📋 Columns: {len(df.columns)}")
    
    print(f"\n🎯 FINAL SUMMARY:")
    print(f"   ✅ 'Out' → 'Out-patient': {df['DEPARTMENT'].eq('Out-patient').sum():,} records")
    print(f"   ✅ 'Inp' → 'In-patient': {df['DEPARTMENT'].eq('In-patient').sum():,} records")
    print(f"   🔧 Leading/trailing spaces cleaned")
    print(f"   📄 Final file: Data_Department_Standardized.csv")
    
else:
    print(f"❌ DEPARTMENT column not found in dataset!")
    print(f"Available columns: {list(df.columns)}")
