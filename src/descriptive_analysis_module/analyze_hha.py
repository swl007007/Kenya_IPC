#!/usr/bin/env python3
"""
Comprehensive Descriptive Analysis of HHA_all.dta
Ignores columns with more than 80% missing values
"""

import pandas as pd
import numpy as np
import sys

def analyze_stata_file(filepath):
    """Load and analyze Stata file with comprehensive statistics"""

    print("=" * 80)
    print("COMPREHENSIVE DESCRIPTIVE ANALYSIS")
    print(f"File: {filepath}")
    print("=" * 80)
    print()

    # Load the Stata file
    print("Loading data...")
    try:
        df = pd.read_stata(filepath)
        print(f"[OK] Data loaded successfully")
        print()
    except Exception as e:
        print(f"[ERROR] Error loading file: {e}")
        sys.exit(1)

    # Basic dataset information
    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)
    print(f"Number of observations: {len(df):,}")
    print(f"Number of variables: {len(df.columns):,}")
    print()

    # Calculate missing percentages
    print("Calculating missing data percentages...")
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)

    # Identify columns with >80% missing
    high_missing_cols = missing_pct[missing_pct > 80].index.tolist()
    valid_cols = missing_pct[missing_pct <= 80].index.tolist()

    print(f"[INFO] Variables with >80% missing: {len(high_missing_cols)}")
    print(f"[INFO] Variables with <=80% missing (analyzed): {len(valid_cols)}")
    print()

    if high_missing_cols:
        print("=" * 80)
        print("EXCLUDED VARIABLES (>80% missing)")
        print("=" * 80)
        for col in high_missing_cols[:20]:  # Show first 20
            print(f"  {col}: {missing_pct[col]:.2f}% missing")
        if len(high_missing_cols) > 20:
            print(f"  ... and {len(high_missing_cols) - 20} more variables")
        print()

    # Filter dataset
    df_analyzed = df[valid_cols].copy()

    # Separate numeric and categorical variables
    numeric_cols = df_analyzed.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df_analyzed.select_dtypes(exclude=[np.number]).columns.tolist()

    print("=" * 80)
    print("VARIABLE TYPES (after filtering)")
    print("=" * 80)
    print(f"Numeric variables: {len(numeric_cols)}")
    print(f"Categorical/String variables: {len(categorical_cols)}")
    print()

    # NUMERIC VARIABLES ANALYSIS
    if numeric_cols:
        print("=" * 80)
        print("NUMERIC VARIABLES - DESCRIPTIVE STATISTICS")
        print("=" * 80)
        print()

        for col in numeric_cols:
            print(f"\n{col}")
            print("-" * 80)

            # Get non-missing values
            valid_data = df_analyzed[col].dropna()
            n_missing = df_analyzed[col].isnull().sum()
            pct_missing = (n_missing / len(df_analyzed)) * 100

            print(f"  Observations: {len(valid_data):,} (Missing: {n_missing:,}, {pct_missing:.2f}%)")

            if len(valid_data) > 0:
                print(f"  Mean: {valid_data.mean():.4f}")
                print(f"  Std Dev: {valid_data.std():.4f}")
                print(f"  Min: {valid_data.min():.4f}")
                print(f"  25th percentile: {valid_data.quantile(0.25):.4f}")
                print(f"  Median: {valid_data.median():.4f}")
                print(f"  75th percentile: {valid_data.quantile(0.75):.4f}")
                print(f"  Max: {valid_data.max():.4f}")
                print(f"  Skewness: {valid_data.skew():.4f}")
                print(f"  Kurtosis: {valid_data.kurtosis():.4f}")

                # Count unique values
                n_unique = valid_data.nunique()
                print(f"  Unique values: {n_unique:,}")

                # If few unique values, show value counts
                if n_unique <= 10:
                    print(f"  Value distribution:")
                    value_counts = valid_data.value_counts().sort_index()
                    for val, count in value_counts.items():
                        pct = (count / len(valid_data)) * 100
                        print(f"    {val}: {count:,} ({pct:.2f}%)")

    # CATEGORICAL VARIABLES ANALYSIS
    if categorical_cols:
        print("\n" + "=" * 80)
        print("CATEGORICAL VARIABLES - FREQUENCY DISTRIBUTIONS")
        print("=" * 80)
        print()

        for col in categorical_cols:
            print(f"\n{col}")
            print("-" * 80)

            valid_data = df_analyzed[col].dropna()
            n_missing = df_analyzed[col].isnull().sum()
            pct_missing = (n_missing / len(df_analyzed)) * 100

            print(f"  Observations: {len(valid_data):,} (Missing: {n_missing:,}, {pct_missing:.2f}%)")

            if len(valid_data) > 0:
                n_unique = valid_data.nunique()
                print(f"  Unique values: {n_unique:,}")

                # Show frequency distribution
                if n_unique <= 50:  # Only show if not too many categories
                    print(f"  Frequency distribution:")
                    value_counts = valid_data.value_counts()
                    for val, count in value_counts.head(20).items():
                        pct = (count / len(valid_data)) * 100
                        # Truncate long values
                        val_str = str(val)[:60]
                        print(f"    {val_str}: {count:,} ({pct:.2f}%)")
                    if len(value_counts) > 20:
                        print(f"    ... and {len(value_counts) - 20} more categories")
                else:
                    print(f"  Top 10 most frequent values:")
                    value_counts = valid_data.value_counts()
                    for val, count in value_counts.head(10).items():
                        pct = (count / len(valid_data)) * 100
                        val_str = str(val)[:60]
                        print(f"    {val_str}: {count:,} ({pct:.2f}%)")

    # SUMMARY STATISTICS TABLE
    print("\n" + "=" * 80)
    print("SUMMARY TABLE - MISSING DATA")
    print("=" * 80)
    print()
    missing_summary = pd.DataFrame({
        'Variable': valid_cols,
        'Missing_Count': [df_analyzed[col].isnull().sum() for col in valid_cols],
        'Missing_Percent': [df_analyzed[col].isnull().sum() / len(df_analyzed) * 100 for col in valid_cols],
        'Type': [df_analyzed[col].dtype for col in valid_cols]
    }).sort_values('Missing_Percent', ascending=False)

    print(missing_summary.to_string(index=False))

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    filepath = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
    analyze_stata_file(filepath)
