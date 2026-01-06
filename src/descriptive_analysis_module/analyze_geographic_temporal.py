#!/usr/bin/env python3
"""
Geographic and Temporal Analysis of HHA_all.dta Panel Dataset
Analyzes household distribution across geographic levels and time periods
"""

import pandas as pd
import numpy as np
import sys
from collections import defaultdict

def analyze_geographic_temporal(filepath):
    """Comprehensive geographic and temporal analysis"""

    print("=" * 100)
    print("GEOGRAPHIC AND TEMPORAL ANALYSIS - HHA_all.dta")
    print("=" * 100)
    print()

    # Load data
    print("Loading data...")
    try:
        df = pd.read_stata(filepath)
        print(f"[OK] Data loaded successfully")
        print(f"Total observations: {len(df):,}")
        print()
    except Exception as e:
        print(f"[ERROR] Error loading file: {e}")
        sys.exit(1)

    # Identify relevant columns
    # Based on previous analysis:
    # b = County
    # c = Sub-county
    # d = Ward
    # e = Livelihood Zone
    # f = Month
    # g = Year
    # qid = Household ID

    county_col = 'b'
    subcounty_col = 'c'
    ward_col = 'd'
    livelihood_col = 'e'
    month_col = 'f'
    year_col = 'g'
    hh_id_col = 'qid'

    # Clean the data - remove blank values
    df_clean = df.copy()
    for col in [county_col, subcounty_col, ward_col, livelihood_col, month_col, year_col]:
        df_clean[col] = df_clean[col].replace('', np.nan)

    # Filter to non-missing geographic/temporal data
    df_panel = df_clean[
        df_clean[county_col].notna() &
        df_clean[year_col].notna()
    ].copy()

    print("=" * 100)
    print("PANEL DATASET STRUCTURE")
    print("=" * 100)
    print(f"Observations with geographic/temporal data: {len(df_panel):,}")
    print(f"Missing geographic/temporal data: {len(df) - len(df_panel):,}")
    print()

    # ========================================================================
    # GEOGRAPHIC DISTRIBUTION ANALYSIS
    # ========================================================================

    print("=" * 100)
    print("GEOGRAPHIC DISTRIBUTION")
    print("=" * 100)
    print()

    # County Level
    print("-" * 100)
    print("1. COUNTY LEVEL DISTRIBUTION")
    print("-" * 100)
    county_dist = df_panel[county_col].value_counts().sort_values(ascending=False)
    print(f"\nTotal unique counties: {len(county_dist)}")
    print(f"\nTop 15 counties by number of observations:")
    print()
    for i, (county, count) in enumerate(county_dist.head(15).items(), 1):
        pct = (count / len(df_panel)) * 100
        print(f"  {i:2d}. {county:25s}: {count:6,} obs ({pct:5.2f}%)")

    if len(county_dist) > 15:
        print(f"  ... and {len(county_dist) - 15} more counties")
    print()

    # Sub-county Level
    print("-" * 100)
    print("2. SUB-COUNTY LEVEL DISTRIBUTION")
    print("-" * 100)
    subcounty_dist = df_panel[subcounty_col].value_counts().sort_values(ascending=False)
    print(f"\nTotal unique sub-counties: {len(subcounty_dist)}")
    print(f"\nTop 20 sub-counties by number of observations:")
    print()
    for i, (subcounty, count) in enumerate(subcounty_dist.head(20).items(), 1):
        pct = (count / len(df_panel)) * 100
        print(f"  {i:2d}. {subcounty:30s}: {count:6,} obs ({pct:5.2f}%)")

    if len(subcounty_dist) > 20:
        print(f"  ... and {len(subcounty_dist) - 20} more sub-counties")
    print()

    # Ward Level
    print("-" * 100)
    print("3. WARD LEVEL DISTRIBUTION")
    print("-" * 100)
    ward_dist = df_panel[ward_col].value_counts().sort_values(ascending=False)
    print(f"\nTotal unique wards: {len(ward_dist)}")
    print(f"\nTop 25 wards by number of observations:")
    print()
    for i, (ward, count) in enumerate(ward_dist.head(25).items(), 1):
        pct = (count / len(df_panel)) * 100
        print(f"  {i:2d}. {ward:35s}: {count:6,} obs ({pct:5.2f}%)")

    if len(ward_dist) > 25:
        print(f"  ... and {len(ward_dist) - 25} more wards")
    print()

    # Livelihood Zone Level
    print("-" * 100)
    print("4. LIVELIHOOD ZONE DISTRIBUTION")
    print("-" * 100)
    lz_dist = df_panel[livelihood_col].value_counts().sort_values(ascending=False)
    print(f"\nTotal unique livelihood zones: {len(lz_dist)}")
    print(f"\nLivelihood zones by number of observations:")
    print()
    for i, (lz, count) in enumerate(lz_dist.items(), 1):
        pct = (count / len(df_panel)) * 100
        print(f"  {i:2d}. {lz:40s}: {count:6,} obs ({pct:5.2f}%)")
    print()

    # ========================================================================
    # TEMPORAL DISTRIBUTION ANALYSIS
    # ========================================================================

    print("=" * 100)
    print("TEMPORAL DISTRIBUTION")
    print("=" * 100)
    print()

    # Year Distribution
    print("-" * 100)
    print("1. YEAR DISTRIBUTION")
    print("-" * 100)
    year_dist = df_panel[year_col].value_counts().sort_index()
    print(f"\nTotal unique years: {len(year_dist)}")
    print(f"\nObservations by year:")
    print()
    for year, count in year_dist.items():
        pct = (count / len(df_panel)) * 100
        print(f"  {year}: {count:8,} obs ({pct:6.2f}%)")
    print()

    # Month Distribution
    print("-" * 100)
    print("2. MONTH DISTRIBUTION")
    print("-" * 100)
    month_dist = df_panel[month_col].value_counts().sort_index()
    print(f"\nTotal unique months: {len(month_dist)}")
    print(f"\nObservations by month:")
    print()
    for month, count in month_dist.items():
        pct = (count / len(df_panel)) * 100
        print(f"  {month:15s}: {count:8,} obs ({pct:6.2f}%)")
    print()

    # Year-Month Distribution
    print("-" * 100)
    print("3. YEAR-MONTH DISTRIBUTION")
    print("-" * 100)
    df_panel['year_month'] = df_panel[year_col].astype(str) + '-' + df_panel[month_col].astype(str)
    yearmonth_dist = df_panel['year_month'].value_counts().sort_index()
    print(f"\nTotal unique year-month combinations: {len(yearmonth_dist)}")
    print(f"\nObservations by year-month:")
    print()
    for ym, count in yearmonth_dist.items():
        pct = (count / len(df_panel)) * 100
        print(f"  {ym:20s}: {count:8,} obs ({pct:6.2f}%)")
    print()

    # ========================================================================
    # PANEL STRUCTURE ANALYSIS
    # ========================================================================

    print("=" * 100)
    print("PANEL STRUCTURE ANALYSIS")
    print("=" * 100)
    print()

    # Number of distinct geographic units by year
    print("-" * 100)
    print("1. DISTINCT GEOGRAPHIC UNITS BY YEAR")
    print("-" * 100)
    print()

    for year in sorted(df_panel[year_col].unique()):
        df_year = df_panel[df_panel[year_col] == year]
        n_counties = df_year[county_col].nunique()
        n_subcounties = df_year[subcounty_col].nunique()
        n_wards = df_year[ward_col].nunique()
        n_lz = df_year[livelihood_col].nunique()
        n_hh = df_year[hh_id_col].nunique()
        n_obs = len(df_year)

        print(f"Year: {year}")
        print(f"  Observations: {n_obs:,}")
        print(f"  Unique households: {n_hh:,}")
        print(f"  Unique counties: {n_counties}")
        print(f"  Unique sub-counties: {n_subcounties}")
        print(f"  Unique wards: {n_wards}")
        print(f"  Unique livelihood zones: {n_lz}")
        print(f"  Avg obs per household: {n_obs/n_hh if n_hh > 0 else 0:.2f}")
        print()

    # Number of distinct geographic units by year-month
    print("-" * 100)
    print("2. DISTINCT GEOGRAPHIC UNITS BY YEAR-MONTH")
    print("-" * 100)
    print()

    for ym in sorted(df_panel['year_month'].unique()):
        df_ym = df_panel[df_panel['year_month'] == ym]
        n_counties = df_ym[county_col].nunique()
        n_subcounties = df_ym[subcounty_col].nunique()
        n_wards = df_ym[ward_col].nunique()
        n_lz = df_ym[livelihood_col].nunique()
        n_hh = df_ym[hh_id_col].nunique()
        n_obs = len(df_ym)

        print(f"Period: {ym}")
        print(f"  Observations: {n_obs:,}")
        print(f"  Unique households: {n_hh:,}")
        print(f"  Unique counties: {n_counties}")
        print(f"  Unique sub-counties: {n_subcounties}")
        print(f"  Unique wards: {n_wards}")
        print(f"  Unique livelihood zones: {n_lz}")
        print(f"  Avg obs per household: {n_obs/n_hh if n_hh > 0 else 0:.2f}")
        print()

    # ========================================================================
    # HOUSEHOLD PANEL STRUCTURE
    # ========================================================================

    print("=" * 100)
    print("HOUSEHOLD PANEL STRUCTURE")
    print("=" * 100)
    print()

    # Count observations per household
    hh_obs_count = df_panel[hh_id_col].value_counts()

    print(f"Total unique households: {len(hh_obs_count):,}")
    print(f"Total observations: {len(df_panel):,}")
    print(f"Average observations per household: {hh_obs_count.mean():.2f}")
    print(f"Median observations per household: {hh_obs_count.median():.0f}")
    print(f"Min observations per household: {hh_obs_count.min()}")
    print(f"Max observations per household: {hh_obs_count.max()}")
    print()

    print("Distribution of observations per household:")
    obs_dist = hh_obs_count.value_counts().sort_index()
    for n_obs, n_hh in obs_dist.items():
        pct = (n_hh / len(hh_obs_count)) * 100
        print(f"  {n_obs:3d} observations: {n_hh:6,} households ({pct:5.2f}%)")
    print()

    # ========================================================================
    # CROSS-TABULATIONS
    # ========================================================================

    print("=" * 100)
    print("GEOGRAPHIC X TEMPORAL CROSS-TABULATIONS")
    print("=" * 100)
    print()

    # Counties by Year
    print("-" * 100)
    print("1. COUNTIES BY YEAR")
    print("-" * 100)
    print()
    county_year = pd.crosstab(df_panel[county_col], df_panel[year_col], margins=True)
    print(county_year.to_string())
    print()

    # Counties by Year-Month
    print("-" * 100)
    print("2. COUNTIES BY YEAR-MONTH")
    print("-" * 100)
    print()
    county_yearmonth = pd.crosstab(df_panel[county_col], df_panel['year_month'], margins=True)
    print(county_yearmonth.to_string())
    print()

    # Livelihood Zones by Year
    print("-" * 100)
    print("3. LIVELIHOOD ZONES BY YEAR")
    print("-" * 100)
    print()
    lz_year = pd.crosstab(df_panel[livelihood_col], df_panel[year_col], margins=True)
    print(lz_year.to_string())
    print()

    # Livelihood Zones by Year-Month
    print("-" * 100)
    print("4. LIVELIHOOD ZONES BY YEAR-MONTH")
    print("-" * 100)
    print()
    lz_yearmonth = pd.crosstab(df_panel[livelihood_col], df_panel['year_month'], margins=True)
    print(lz_yearmonth.to_string())
    print()

    # ========================================================================
    # GEOGRAPHIC HIERARCHY ANALYSIS
    # ========================================================================

    print("=" * 100)
    print("GEOGRAPHIC HIERARCHY ANALYSIS")
    print("=" * 100)
    print()

    # Sub-counties per county
    print("-" * 100)
    print("SUB-COUNTIES PER COUNTY")
    print("-" * 100)
    print()
    county_subcounty = df_panel.groupby(county_col)[subcounty_col].nunique().sort_values(ascending=False)
    for county, n_subcounties in county_subcounty.items():
        print(f"  {county:25s}: {n_subcounties:3d} sub-counties")
    print()

    # Wards per county
    print("-" * 100)
    print("WARDS PER COUNTY")
    print("-" * 100)
    print()
    county_ward = df_panel.groupby(county_col)[ward_col].nunique().sort_values(ascending=False)
    for county, n_wards in county_ward.items():
        print(f"  {county:25s}: {n_wards:3d} wards")
    print()

    # Livelihood zones per county
    print("-" * 100)
    print("LIVELIHOOD ZONES PER COUNTY")
    print("-" * 100)
    print()
    county_lz = df_panel.groupby(county_col)[livelihood_col].nunique().sort_values(ascending=False)
    for county, n_lz in county_lz.items():
        print(f"  {county:25s}: {n_lz:2d} livelihood zones")
    print()

    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================

    print("=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)
    print()

    summary_stats = {
        'Total Observations': len(df_panel),
        'Unique Households': df_panel[hh_id_col].nunique(),
        'Unique Counties': df_panel[county_col].nunique(),
        'Unique Sub-counties': df_panel[subcounty_col].nunique(),
        'Unique Wards': df_panel[ward_col].nunique(),
        'Unique Livelihood Zones': df_panel[livelihood_col].nunique(),
        'Unique Years': df_panel[year_col].nunique(),
        'Unique Months': df_panel[month_col].nunique(),
        'Unique Year-Month Periods': df_panel['year_month'].nunique(),
        'Date Range': f"{df_panel['year_month'].min()} to {df_panel['year_month'].max()}",
        'Avg Obs per Household': f"{len(df_panel) / df_panel[hh_id_col].nunique():.2f}",
        'Avg Households per County': f"{df_panel[hh_id_col].nunique() / df_panel[county_col].nunique():.2f}",
        'Avg Households per Ward': f"{df_panel[hh_id_col].nunique() / df_panel[ward_col].nunique():.2f}",
    }

    for key, value in summary_stats.items():
        print(f"  {key:30s}: {value}")
    print()

    print("=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

    return df_panel, summary_stats

if __name__ == "__main__":
    filepath = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
    df_panel, summary = analyze_geographic_temporal(filepath)
