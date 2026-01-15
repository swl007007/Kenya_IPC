#!/usr/bin/env python3
"""
Comprehensive Geographic and Temporal Analysis of HHA_all.dta Panel Dataset
Uses proper column names and analyzes the full panel structure
"""

import pandas as pd
import numpy as np
import sys
import os

def analyze_panel(filepath):
    """Comprehensive geographic and temporal analysis"""

    print("=" * 120)
    print("GEOGRAPHIC AND TEMPORAL ANALYSIS - HHA_all.dta PANEL DATASET")
    print("=" * 120)
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

    # Use proper column names
    county_col = 'county'
    subcounty_col = 'subcounty'
    ward_col = 'ward'
    livelihood_col = 'livelihoodzone'
    month_col = 'month'
    year_col = 'year'
    hh_code_col = 'householdcode'
    hh_id_col = 'qid'
    date_col = 'interviewdate'

    print("=" * 120)
    print("DATASET STRUCTURE")
    print("=" * 120)

    # Check both qid and householdcode as potential household identifiers
    qid_populated = df[hh_id_col].notna() & (df[hh_id_col] != '')
    hhcode_populated = df[hh_code_col].notna() & (df[hh_code_col] != '')

    print(f"Rows with qid populated: {qid_populated.sum():,}")
    print(f"Rows with householdcode populated: {hhcode_populated.sum():,}")
    print(f"Rows with year data: {(df[year_col].notna() & (df[year_col] != '')).sum():,}")
    print()

    # Filter to rows with valid temporal data
    df_panel = df[(df[year_col].notna()) & (df[year_col] != '') & (df[year_col] != 'Year')].copy()

    print(f"Panel dataset (with valid year): {len(df_panel):,} observations")
    print()

    # Determine household identifier
    # Use householdcode for panel, qid for cross-section
    df_panel['hh_identifier'] = df_panel[hh_code_col].fillna(df_panel[hh_id_col])

    # ========================================================================
    # TEMPORAL DISTRIBUTION
    # ========================================================================

    print("=" * 120)
    print("1. TEMPORAL DISTRIBUTION")
    print("=" * 120)
    print()

    # Year distribution
    print("-" * 120)
    print("1.1 YEAR DISTRIBUTION")
    print("-" * 120)
    year_dist = df_panel[year_col].value_counts().sort_index()
    print(f"\nTotal unique years: {len(year_dist)}")
    print(f"\nObservations by year:")
    for year, count in year_dist.items():
        pct = (count / len(df_panel)) * 100
        n_hh = df_panel[df_panel[year_col] == year]['hh_identifier'].nunique()
        print(f"  {year:10s}: {count:8,} observations ({pct:6.2f}%) | {n_hh:,} unique households")
    print()

    # Month distribution
    print("-" * 120)
    print("1.2 MONTH DISTRIBUTION")
    print("-" * 120)
    month_dist = df_panel[month_col].value_counts()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    print(f"\nTotal unique months: {len(month_dist)}")
    print(f"\nObservations by month:")
    for month in month_order:
        if month in month_dist.index:
            count = month_dist[month]
            pct = (count / len(df_panel)) * 100
            n_hh = df_panel[df_panel[month_col] == month]['hh_identifier'].nunique()
            print(f"  {month:15s}: {count:8,} observations ({pct:6.2f}%) | {n_hh:,} unique households")
    print()

    # Year-Month distribution
    print("-" * 120)
    print("1.3 YEAR-MONTH DISTRIBUTION")
    print("-" * 120)
    df_panel['year_month'] = df_panel[year_col].astype(str) + '-' + df_panel[month_col].astype(str)

    yearmonth_counts = df_panel['year_month'].value_counts().sort_index()

    print(f"\nTotal unique year-month combinations: {len(yearmonth_counts)}")
    print(f"\nObservations by year-month:")
    print(f"{'Period':<20s} {'Observations':>15s} {'Unique HH':>15s} {'Avg Obs/HH':>15s}")
    print("-" * 70)
    for ym in sorted(yearmonth_counts.index):
        obs = len(df_panel[df_panel['year_month'] == ym])
        hh = df_panel[df_panel['year_month'] == ym]['hh_identifier'].nunique()
        avg = obs / hh if hh > 0 else 0
        print(f"{ym:<20s} {obs:>15,} {hh:>15,} {avg:>15.2f}")
    print()

    # Interview date distribution
    print("-" * 120)
    print("1.4 INTERVIEW DATE DISTRIBUTION")
    print("-" * 120)
    date_dist = df_panel[date_col].value_counts().sort_index()
    print(f"\nTotal unique interview dates: {len(date_dist)}")
    print(f"\nTop 20 interview dates:")
    for date, count in date_dist.head(20).items():
        print(f"  {date}: {count:,} observations")
    print()

    # ========================================================================
    # GEOGRAPHIC DISTRIBUTION
    # ========================================================================

    print("=" * 120)
    print("2. GEOGRAPHIC DISTRIBUTION")
    print("=" * 120)
    print()

    # County Level
    print("-" * 120)
    print("2.1 COUNTY LEVEL")
    print("-" * 120)
    county_stats = df_panel.groupby(county_col).agg({
        'hh_identifier': ['count', 'nunique']
    })
    county_stats.columns = ['observations', 'unique_hh']
    county_stats = county_stats.sort_values('observations', ascending=False)

    print(f"\nTotal unique counties: {len(county_stats)}")
    print(f"\n{'County':<30s} {'Observations':>15s} {'Unique HH':>15s} {'% of Total':>12s}")
    print("-" * 75)
    for county, row in county_stats.iterrows():
        pct = (row['observations'] / len(df_panel)) * 100
        print(f"{str(county):<30s} {row['observations']:>15,.0f} {row['unique_hh']:>15,.0f} {pct:>11.2f}%")
    print()

    # Sub-county Level
    print("-" * 120)
    print("2.2 SUB-COUNTY LEVEL")
    print("-" * 120)
    subcounty_stats = df_panel.groupby(subcounty_col).agg({
        'hh_identifier': ['count', 'nunique']
    })
    subcounty_stats.columns = ['observations', 'unique_hh']
    subcounty_stats = subcounty_stats.sort_values('observations', ascending=False)

    print(f"\nTotal unique sub-counties: {len(subcounty_stats)}")
    print(f"\nTop 25 sub-counties:")
    print(f"{'Sub-county':<35s} {'Observations':>15s} {'Unique HH':>15s} {'% of Total':>12s}")
    print("-" * 80)
    for subcounty, row in subcounty_stats.head(25).iterrows():
        pct = (row['observations'] / len(df_panel)) * 100
        print(f"{str(subcounty):<35s} {row['observations']:>15,.0f} {row['unique_hh']:>15,.0f} {pct:>11.2f}%")
    if len(subcounty_stats) > 25:
        print(f"\n... and {len(subcounty_stats) - 25} more sub-counties")
    print()

    # Ward Level
    print("-" * 120)
    print("2.3 WARD LEVEL")
    print("-" * 120)
    ward_stats = df_panel.groupby(ward_col).agg({
        'hh_identifier': ['count', 'nunique']
    })
    ward_stats.columns = ['observations', 'unique_hh']
    ward_stats = ward_stats.sort_values('observations', ascending=False)

    print(f"\nTotal unique wards: {len(ward_stats)}")
    print(f"\nTop 25 wards:")
    print(f"{'Ward':<40s} {'Observations':>15s} {'Unique HH':>15s} {'% of Total':>12s}")
    print("-" * 85)
    for ward, row in ward_stats.head(25).iterrows():
        pct = (row['observations'] / len(df_panel)) * 100
        print(f"{str(ward):<40s} {row['observations']:>15,.0f} {row['unique_hh']:>15,.0f} {pct:>11.2f}%")
    if len(ward_stats) > 25:
        print(f"\n... and {len(ward_stats) - 25} more wards")
    print()

    # Livelihood Zone Level
    print("-" * 120)
    print("2.4 LIVELIHOOD ZONE LEVEL")
    print("-" * 120)
    lz_stats = df_panel.groupby(livelihood_col).agg({
        'hh_identifier': ['count', 'nunique']
    })
    lz_stats.columns = ['observations', 'unique_hh']
    lz_stats = lz_stats.sort_values('observations', ascending=False)

    print(f"\nTotal unique livelihood zones: {len(lz_stats)}")
    print(f"\n{'Livelihood Zone':<45s} {'Observations':>15s} {'Unique HH':>15s} {'% of Total':>12s}")
    print("-" * 90)
    for lz, row in lz_stats.iterrows():
        pct = (row['observations'] / len(df_panel)) * 100
        print(f"{str(lz):<45s} {row['observations']:>15,.0f} {row['unique_hh']:>15,.0f} {pct:>11.2f}%")
    print()

    # ========================================================================
    # PANEL STRUCTURE
    # ========================================================================

    print("=" * 120)
    print("3. PANEL STRUCTURE ANALYSIS")
    print("=" * 120)
    print()

    # Household observation counts
    hh_obs_count = df_panel['hh_identifier'].value_counts()

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
        print(f"  {n_obs:3d} observation(s): {n_hh:6,} households ({pct:5.2f}%)")
    print()

    # ========================================================================
    # TEMPORAL X GEOGRAPHIC CROSS-TABS
    # ========================================================================

    print("=" * 120)
    print("4. GEOGRAPHIC × TEMPORAL CROSS-TABULATIONS")
    print("=" * 120)
    print()

    # Counties by Year-Month
    print("-" * 120)
    print("4.1 COUNTIES BY YEAR-MONTH (Observations)")
    print("-" * 120)
    county_ym_obs = pd.crosstab(df_panel[county_col], df_panel['year_month'], margins=True)
    print(county_ym_obs.to_string())
    print("\n")

    # Counties by Year-Month (Unique Households)
    print("-" * 120)
    print("4.2 COUNTIES BY YEAR-MONTH (Unique Households)")
    print("-" * 120)
    county_ym_hh = df_panel.groupby([county_col, 'year_month'])['hh_identifier'].nunique().unstack(fill_value=0)
    county_ym_hh.loc['Total'] = county_ym_hh.sum()
    county_ym_hh['Total'] = county_ym_hh.sum(axis=1)
    print(county_ym_hh.to_string())
    print("\n")

    # Livelihood Zones by Year-Month
    print("-" * 120)
    print("4.3 LIVELIHOOD ZONES BY YEAR-MONTH (Observations)")
    print("-" * 120)
    lz_ym_obs = pd.crosstab(df_panel[livelihood_col], df_panel['year_month'], margins=True)
    print(lz_ym_obs.to_string())
    print("\n")

    # Livelihood Zones by Year-Month (Unique Households)
    print("-" * 120)
    print("4.4 LIVELIHOOD ZONES BY YEAR-MONTH (Unique Households)")
    print("-" * 120)
    lz_ym_hh = df_panel.groupby([livelihood_col, 'year_month'])['hh_identifier'].nunique().unstack(fill_value=0)
    lz_ym_hh.loc['Total'] = lz_ym_hh.sum()
    lz_ym_hh['Total'] = lz_ym_hh.sum(axis=1)
    print(lz_ym_hh.to_string())
    print("\n")

    # ========================================================================
    # EXPORT DETAILED CROSSTABS TO EXCEL
    # ========================================================================

    print("-" * 120)
    print("EXPORTING DETAILED CROSSTABS TO EXCEL")
    print("-" * 120)
    print()

    # Determine output directory (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'output')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # 4.5 - Subcounty by Year-Month (Unique Households)
    print("Generating Subcounty × Year-Month crosstab (Unique Households)...")
    subcounty_ym_hh = df_panel.groupby([subcounty_col, 'year_month'])['hh_identifier'].nunique().unstack(fill_value=0)
    subcounty_ym_hh.loc['Total'] = subcounty_ym_hh.sum()
    subcounty_ym_hh['Total'] = subcounty_ym_hh.sum(axis=1)

    # Export to Excel
    subcounty_excel_file = os.path.join(output_dir, 'subcounty_by_yearmonth_unique_households.xlsx')
    subcounty_ym_hh.to_excel(subcounty_excel_file, sheet_name='Subcounty_YearMonth')
    print(f"  [OK] Exported to: {subcounty_excel_file}")
    print(f"  Dimensions: {len(subcounty_ym_hh)} subcounties × {len(subcounty_ym_hh.columns)} periods")
    print()

    # 4.6 - Ward by Year-Month (Unique Households)
    print("Generating Ward × Year-Month crosstab (Unique Households)...")
    ward_ym_hh = df_panel.groupby([ward_col, 'year_month'])['hh_identifier'].nunique().unstack(fill_value=0)
    ward_ym_hh.loc['Total'] = ward_ym_hh.sum()
    ward_ym_hh['Total'] = ward_ym_hh.sum(axis=1)

    # Export to Excel
    ward_excel_file = os.path.join(output_dir, 'ward_by_yearmonth_unique_households.xlsx')
    ward_ym_hh.to_excel(ward_excel_file, sheet_name='Ward_YearMonth')
    print(f"  [OK] Exported to: {ward_excel_file}")
    print(f"  Dimensions: {len(ward_ym_hh)} wards × {len(ward_ym_hh.columns)} periods")
    print()

    print("-" * 120)
    print()

    # ========================================================================
    # GEOGRAPHIC HIERARCHY
    # ========================================================================

    print("=" * 120)
    print("5. GEOGRAPHIC HIERARCHY ANALYSIS")
    print("=" * 120)
    print()

    # Sub-counties per county
    print("-" * 120)
    print("5.1 SUB-COUNTIES PER COUNTY")
    print("-" * 120)
    county_subcounty = df_panel.groupby(county_col)[subcounty_col].nunique().sort_values(ascending=False)
    for county, n_subcounties in county_subcounty.items():
        n_obs = len(df_panel[df_panel[county_col] == county])
        n_hh = df_panel[df_panel[county_col] == county]['hh_identifier'].nunique()
        print(f"  {str(county):<30s}: {n_subcounties:3d} sub-counties | {n_obs:6,} obs | {n_hh:5,} HH")
    print()

    # Wards per county
    print("-" * 120)
    print("5.2 WARDS PER COUNTY")
    print("-" * 120)
    county_ward = df_panel.groupby(county_col)[ward_col].nunique().sort_values(ascending=False)
    for county, n_wards in county_ward.items():
        n_obs = len(df_panel[df_panel[county_col] == county])
        n_hh = df_panel[df_panel[county_col] == county]['hh_identifier'].nunique()
        print(f"  {str(county):<30s}: {n_wards:3d} wards | {n_obs:6,} obs | {n_hh:5,} HH")
    print()

    # Livelihood zones per county
    print("-" * 120)
    print("5.3 LIVELIHOOD ZONES PER COUNTY")
    print("-" * 120)
    county_lz = df_panel.groupby(county_col)[livelihood_col].nunique().sort_values(ascending=False)
    for county, n_lz in county_lz.items():
        lz_list = df_panel[df_panel[county_col] == county][livelihood_col].unique()
        print(f"  {str(county):<30s}: {n_lz:2d} livelihood zones")
        for lz in sorted(lz_list):
            n_obs = len(df_panel[(df_panel[county_col] == county) & (df_panel[livelihood_col] == lz)])
            print(f"      - {str(lz):<40s}: {n_obs:5,} obs")
    print()

    # ========================================================================
    # WARD-LEVEL TEMPORAL ANALYSIS
    # ========================================================================

    print("=" * 120)
    print("5A. WARD-LEVEL TEMPORAL ANALYSIS")
    print("=" * 120)
    print()

    # 5A.1 - Wards per month
    print("-" * 120)
    print("5A.1 WARDS OBSERVED PER MONTH (Across All Years)")
    print("-" * 120)

    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    wards_by_month = df_panel.groupby(month_col)[ward_col].nunique()

    print(f"\n{'Month':<20s} {'Unique Wards':>15s}")
    print("-" * 40)
    for month in month_order:
        if month in wards_by_month.index:
            count = wards_by_month[month]
            print(f"{month:<20s} {count:>15,}")
    print()

    # 5A.2 - Average households per ward per month
    print("-" * 120)
    print("5A.2 AVERAGE HOUSEHOLDS PER WARD PER MONTH")
    print("-" * 120)

    # Calculate ward-month-household counts
    ward_month_hh = df_panel.groupby([ward_col, month_col])['hh_identifier'].nunique().reset_index()
    ward_month_hh.columns = ['ward', 'month', 'unique_hh']

    # Average per ward across months
    avg_hh_per_ward = ward_month_hh.groupby('ward')['unique_hh'].mean().sort_values(ascending=False)

    # Active months per ward
    months_per_ward = ward_month_hh.groupby('ward')['month'].count()

    # Total observations per ward
    obs_per_ward = df_panel.groupby(ward_col).size()

    # Distribution statistics
    print("\nDistribution of Average Households per Ward per Month:")
    print(f"  Mean:       {avg_hh_per_ward.mean():>7.2f} households")
    print(f"  Median:     {avg_hh_per_ward.median():>7.2f} households")
    print(f"  Min:        {avg_hh_per_ward.min():>7.2f} households")
    print(f"  Max:        {avg_hh_per_ward.max():>7.2f} households")
    print(f"  25th %ile:  {avg_hh_per_ward.quantile(0.25):>7.2f} households")
    print(f"  75th %ile:  {avg_hh_per_ward.quantile(0.75):>7.2f} households")
    print()

    # Top 25 wards
    print(f"\nTop 25 Wards by Average Households per Month:")
    print(f"{'Ward':<40s} {'Avg HH/Month':>15s} {'Total Obs':>15s} {'Active Months':>15s}")
    print("-" * 90)
    for ward in avg_hh_per_ward.head(25).index:
        avg_hh = avg_hh_per_ward[ward]
        total_obs = obs_per_ward[ward]
        active_months = months_per_ward[ward]
        print(f"{str(ward):<40s} {avg_hh:>15.2f} {total_obs:>15,} {active_months:>15,}")
    print()

    # Distribution histogram
    bins = [0, 10, 20, 30, 40, 50, float('inf')]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '50+']
    ward_distribution = pd.cut(avg_hh_per_ward, bins=bins, labels=labels).value_counts().sort_index()

    print("\nDistribution Histogram:")
    print(f"{'Avg HH Range':<20s} {'Number of Wards':>20s} {'% of Wards':>15s}")
    print("-" * 60)
    for range_label, count in ward_distribution.items():
        pct = (count / len(avg_hh_per_ward)) * 100
        print(f"{range_label:<20s} {count:>20,} {pct:>14.1f}%")
    print()

    # ========================================================================
    # SUBCOUNTY-LEVEL TEMPORAL ANALYSIS
    # ========================================================================

    print("=" * 120)
    print("5B. SUBCOUNTY-LEVEL TEMPORAL ANALYSIS")
    print("=" * 120)
    print()

    # 5B.1 - Subcounties per month
    print("-" * 120)
    print("5B.1 SUBCOUNTIES OBSERVED PER MONTH (Across All Years)")
    print("-" * 120)

    subcounties_by_month = df_panel.groupby(month_col)[subcounty_col].nunique()

    print(f"\n{'Month':<20s} {'Unique Subcounties':>20s}")
    print("-" * 45)
    for month in month_order:
        if month in subcounties_by_month.index:
            count = subcounties_by_month[month]
            print(f"{month:<20s} {count:>20,}")
    print()

    # 5B.2 - Average households per subcounty per month
    print("-" * 120)
    print("5B.2 AVERAGE HOUSEHOLDS PER SUBCOUNTY PER MONTH")
    print("-" * 120)

    # Calculate subcounty-month-household counts
    subcounty_month_hh = df_panel.groupby([subcounty_col, month_col])['hh_identifier'].nunique().reset_index()
    subcounty_month_hh.columns = ['subcounty', 'month', 'unique_hh']

    # Average per subcounty across months
    avg_hh_per_subcounty = subcounty_month_hh.groupby('subcounty')['unique_hh'].mean().sort_values(ascending=False)

    # Active months per subcounty
    months_per_subcounty = subcounty_month_hh.groupby('subcounty')['month'].count()

    # Total observations per subcounty
    obs_per_subcounty = df_panel.groupby(subcounty_col).size()

    # Distribution statistics
    print("\nDistribution of Average Households per Subcounty per Month:")
    print(f"  Mean:       {avg_hh_per_subcounty.mean():>7.2f} households")
    print(f"  Median:     {avg_hh_per_subcounty.median():>7.2f} households")
    print(f"  Min:        {avg_hh_per_subcounty.min():>7.2f} households")
    print(f"  Max:        {avg_hh_per_subcounty.max():>7.2f} households")
    print(f"  25th %ile:  {avg_hh_per_subcounty.quantile(0.25):>7.2f} households")
    print(f"  75th %ile:  {avg_hh_per_subcounty.quantile(0.75):>7.2f} households")
    print()

    # Top 25 subcounties
    print(f"\nTop 25 Subcounties by Average Households per Month:")
    print(f"{'Subcounty':<40s} {'Avg HH/Month':>15s} {'Total Obs':>15s} {'Active Months':>15s}")
    print("-" * 90)
    for subcounty in avg_hh_per_subcounty.head(25).index:
        avg_hh = avg_hh_per_subcounty[subcounty]
        total_obs = obs_per_subcounty[subcounty]
        active_months = months_per_subcounty[subcounty]
        print(f"{str(subcounty):<40s} {avg_hh:>15.2f} {total_obs:>15,} {active_months:>15,}")
    print()

    # Distribution histogram
    subcounty_distribution = pd.cut(avg_hh_per_subcounty, bins=bins, labels=labels).value_counts().sort_index()

    print("\nDistribution Histogram:")
    print(f"{'Avg HH Range':<20s} {'Number of Subcounties':>25s} {'% of Subcounties':>20s}")
    print("-" * 70)
    for range_label, count in subcounty_distribution.items():
        pct = (count / len(avg_hh_per_subcounty)) * 100
        print(f"{range_label:<20s} {count:>25,} {pct:>19.1f}%")
    print()

    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================

    print("=" * 120)
    print("6. SUMMARY STATISTICS")
    print("=" * 120)
    print()

    summary_stats = {
        'Total Observations': f"{len(df_panel):,}",
        'Unique Households': f"{df_panel['hh_identifier'].nunique():,}",
        'Unique Counties': f"{df_panel[county_col].nunique()}",
        'Unique Sub-counties': f"{df_panel[subcounty_col].nunique()}",
        'Unique Wards': f"{df_panel[ward_col].nunique()}",
        'Unique Livelihood Zones': f"{df_panel[livelihood_col].nunique()}",
        'Unique Years': f"{df_panel[year_col].nunique()}",
        'Unique Months': f"{df_panel[month_col].nunique()}",
        'Unique Year-Month Periods': f"{df_panel['year_month'].nunique()}",
        'Date Range': f"{df_panel['year_month'].min()} to {df_panel['year_month'].max()}",
        'Avg Observations per Household': f"{len(df_panel) / df_panel['hh_identifier'].nunique():.2f}",
        'Avg Households per County': f"{df_panel['hh_identifier'].nunique() / df_panel[county_col].nunique():.2f}",
        'Avg Households per Sub-county': f"{df_panel['hh_identifier'].nunique() / df_panel[subcounty_col].nunique():.2f}",
        'Avg Households per Ward': f"{df_panel['hh_identifier'].nunique() / df_panel[ward_col].nunique():.2f}",
    }

    for key, value in summary_stats.items():
        print(f"  {key:<35s}: {value}")
    print()

    print("=" * 120)
    print("ANALYSIS COMPLETE")
    print("=" * 120)

    return df_panel

if __name__ == "__main__":
    filepath = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
    df_panel = analyze_panel(filepath)
