#!/usr/bin/env python3
"""
Explore the data structure of HHA_all.dta to identify proper panel structure
"""

import pandas as pd
import numpy as np

filepath = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"

print("Loading data...")
df = pd.read_stata(filepath)
print(f"Total observations: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print()

# Show all column names
print("=" * 100)
print("ALL COLUMN NAMES")
print("=" * 100)
for i, col in enumerate(df.columns, 1):
    print(f"{i:3d}. {col}")
print()

# Identify potential ID and temporal columns
print("=" * 100)
print("KEY COLUMNS ANALYSIS")
print("=" * 100)

# Check qid
print("\n1. 'qid' column:")
print(f"   Unique values: {df['qid'].nunique():,}")
print(f"   Non-blank values: {(df['qid'] != '').sum():,}")
print(f"   Blank values: {(df['qid'] == '').sum():,}")
print(f"   Sample values (first 20 non-blank):")
qid_nonblank = df[df['qid'] != '']['qid'].head(20)
for val in qid_nonblank:
    print(f"      {val}")

# Check if there's an hhadata column
hhadata_cols = [col for col in df.columns if 'hhadata' in col.lower() or 'hha' in col.lower()]
print(f"\n2. Columns with 'hha' or 'hhadata':")
for col in hhadata_cols[:10]:
    nunique = df[col].nunique()
    non_blank = (df[col] != '').sum() if df[col].dtype == 'object' else df[col].notna().sum()
    print(f"   {col}: {nunique:,} unique values, {non_blank:,} non-missing")

# Check year column (g)
print(f"\n3. Year column 'g':")
print(f"   Unique values: {df['g'].nunique()}")
print(f"   Value counts:")
year_counts = df['g'].value_counts()
for val, count in year_counts.items():
    print(f"      {val}: {count:,}")

# Check month column (f)
print(f"\n4. Month column 'f':")
print(f"   Unique values: {df['f'].nunique()}")
print(f"   Value counts:")
month_counts = df['f'].value_counts()
for val, count in month_counts.items():
    print(f"      {val}: {count:,}")

# Check date column (j)
print(f"\n5. Date column 'j':")
print(f"   Unique values: {df['j'].nunique()}")
print(f"   Sample values (first 20 non-blank):")
j_nonblank = df[df['j'] != '']['j'].head(20)
for val in j_nonblank:
    print(f"      {val}")

# Look for any numeric ID columns
print("\n6. Potential numeric ID columns:")
for col in df.columns:
    if 'id' in col.lower() and df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
        nunique = df[col].nunique()
        non_missing = df[col].notna().sum()
        print(f"   {col}: {nunique:,} unique, {non_missing:,} non-missing")
        if nunique < 20:
            print(f"      Values: {sorted(df[col].dropna().unique())}")

# Check k column (cluster/enumeration area?)
print(f"\n7. Column 'k' (potential cluster ID):")
print(f"   Unique values: {df['k'].nunique():,}")
print(f"   Non-blank values: {(df['k'] != '').sum():,}")
print(f"   Sample values (first 10 non-blank):")
k_nonblank = df[df['k'] != '']['k'].head(10)
for val in k_nonblank:
    print(f"      {val}")

# Create a year-month combination and see distribution
print("\n" + "=" * 100)
print("TEMPORAL ANALYSIS")
print("=" * 100)

df_temp = df[(df['g'] != '') & (df['g'] != 'Year')].copy()
print(f"\nRows with valid year data: {len(df_temp):,}")

if len(df_temp) > 0:
    df_temp['year_month'] = df_temp['g'].astype(str) + '-' + df_temp['f'].astype(str)
    ym_counts = df_temp['year_month'].value_counts().sort_index()
    print(f"\nYear-Month distribution:")
    for ym, count in ym_counts.items():
        print(f"   {ym}: {count:,}")

    # Check if same households appear in different months
    print("\n" + "=" * 100)
    print("PANEL STRUCTURE CHECK")
    print("=" * 100)

    # Group by qid and see if they appear in multiple time periods
    qid_temp = df_temp[df_temp['qid'] != ''].copy()
    print(f"\nRows with valid qid and temporal data: {len(qid_temp):,}")

    if len(qid_temp) > 0:
        qid_periods = qid_temp.groupby('qid')['year_month'].nunique()
        print(f"\nHouseholds appearing in multiple periods:")
        multi_period = qid_periods[qid_periods > 1]
        print(f"   Count: {len(multi_period):,}")
        if len(multi_period) > 0:
            print(f"\nDistribution of periods per household:")
            period_dist = qid_periods.value_counts().sort_index()
            for n_periods, n_hh in period_dist.items():
                print(f"   {n_periods} periods: {n_hh:,} households")
