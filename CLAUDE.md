# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project analyzing household survey data from Kenya's Arid and Semi-Arid Lands (ASAL) regions. The project focuses on food security analysis using the Integrated Food Security Phase Classification (IPC) methodology.

**Primary Dataset**: `HHA_all.dta` - A longitudinal panel dataset covering 375,959 household observations across 23 counties in Kenya from 2016-2023.

**Key Research Goals**:
- Analyze household food security indicators: rCSI (reduced Coping Strategy Index), LCS (Livelihood Coping Strategies), and FCS (Food Consumption Score)
- Generate preliminary IPC classifications from coping strategies and food consumption indicators
- Conduct geographic and temporal analysis of food security patterns across counties, sub-counties, wards, livelihood zones, months, and years

## Repository Structure

```
Kenya_IPC/
├── src/
│   ├── descriptive_analysis_module/          # Exploratory analysis scripts
│   │   ├── analyze_hha.py                    # Comprehensive descriptive statistics
│   │   ├── explore_data_structure.py         # Dataset structure and panel identifier exploration
│   │   └── geographic_temporal_analysis.py   # Geographic/temporal panel analysis and Excel exports
│   └── IPC_variable/
│       └── genearte_IPC_variable.ipynb       # IPC variable calculation notebook
├── doc/                                      # Analysis reports
│   ├── Geographic_Temporal.txt               # Geographic/temporal analysis report
│   └── HHA_all_other_descriptive_analysis.md # Comprehensive descriptive analysis report
├── output/                                   # Generated visualizations and tables
│   ├── FCS_IPC.png
│   ├── LCS_FCS.png
│   ├── LCS_IPC.png
│   ├── preliminary_IPC.png
│   ├── rCSI_FCS.png
│   ├── rCSI_IPC.png
│   ├── rCSI_LCS.png
│   ├── rCSI_LCS_confusion_matrix.png
│   ├── subcounty_by_yearmonth_unique_households.xlsx
│   └── ward_by_yearmonth_unique_households.xlsx
└── .specify/                                 # Spec Kit scaffolding and templates
```

## Data Structure

### Dataset: HHA_all.dta

**Panel Structure**:
- **Household ID**: `qid` or `householdcode`
- **Time dimensions**: `year` (2016-2023), `month` (monthly observations), `interviewdate`
- **Geographic hierarchy**: `county` → `subcounty` → `ward`
- **Livelihood zones**: `livelihoodzone` (Pastoral, Mixed Farming, Agro Pastoral, etc.)

**Column names**: The current analysis scripts use descriptive column names:
- `county` - County name
- `subcounty` - Sub-county name
- `ward` - Ward name
- `livelihoodzone` - Livelihood zone classification
- `month` - Month name (January, February, etc.)
- `year` - Year (2016-2023)
- `interviewdate` - Interview date
- `householdcode`, `qid` - Household identifiers

`explore_data_structure.py` also references older/raw positional columns such as `f`, `g`, `j`, and `k` when exploring the Stata file structure.

### Key Variable Categories

**Consumption coping strategy variables used for rCSI**:
- `csi_reliedonless`
- `csi_borrowedfood`
- `csi_reducednoofmeals`
- `csi_reducedportionmealsize`
- `csi_quantityforadult`

**Livelihood coping strategy variables used for LCS_IPC**:
- Stress: `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldmoreanimals`
- Crisis: `csi_soldhouseholdassets`, `csi_reducednonfoodexpenses`, `csi_soldproductiveassets`, `csi_withdrewchildrenschool`
- Emergency: `csi_soldhouseland`, `csi_soldlastfemaleanimal`, `csi_begging`

**Food consumption variables used for FCS**:
- Staples: `hfc_graindays`, `hfc_rootsdays`
- Pulses/nuts: `hfc_pulsesnutsdays`
- Dairy: `hfc_milkdays`
- Protein: `hfc_meatdays`, `hfc_liverdays`, `hfc_fishdays`, `hfc_eggsdays`
- Vegetables: `hfc_orangevegdays`, `hfc_greenleafydays`, `hfc_othervegdays`
- Fruits: `hfc_orangefruitsdays`, `hfc_otherfruitsdays`
- Fat, sugar, condiments: `hfc_oildays`, `hfc_sugardays`, `hfc_condimentsdays`

**Water access variables**: `watersource*`, `normalwatersource`, `distancefromwatersource`, `hhpayforwater`

## IPC Calculation Methodology

### rCSI (reduced Coping Strategy Index)
```python
rCSI = (1 * csi_reliedonless +
        2 * csi_borrowedfood +
        1 * csi_reducednoofmeals +
        1 * csi_reducedportionmealsize +
        3 * csi_quantityforadult)
```

**IPC Classification from rCSI**:
- Phase 1 (Minimal): rCSI 0-3
- Phase 2 (Stressed): rCSI 4-18
- Phase 3 (Crisis+): rCSI >= 19

### LCS_IPC (Livelihood Coping Strategies)
Classify household livelihood coping strategies into severity levels:
- **Phase 1 (Minimal)**: No significant coping (value = 0, recoded to 1)
- **Phase 2 (Stress)**: `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldmoreanimals`
- **Phase 3 (Crisis)**: `csi_soldhouseholdassets`, `csi_reducednonfoodexpenses`, `csi_soldproductiveassets`, `csi_withdrewchildrenschool`
- **Phase 4 (Emergency)**: `csi_soldhouseland`, `csi_soldlastfemaleanimal`, `csi_begging`

`LCS_IPC` is the maximum severity across all livelihood coping strategies after recoding 0 to Phase 1.

### FCS (Food Consumption Score)
```python
FCS = (FCSStap * 2 +
       FCSPulse * 3 +
       FCSDairy * 4 +
       FCSPr * 4 +
       FCSVeg * 1 +
       FCSFruits * 1 +
       FCSFat * 0.5 +
       FCSSugar * 0.5)
```

Food groups are constructed from the maximum days consumed within each group where multiple source variables exist.

**IPC Classification from FCS**:
- Phase 1 (Minimal): FCS > 35
- Phase 3 (Crisis): FCS > 21 and <= 35
- Phase 4 (Emergency): FCS <= 21

### Preliminary IPC
The current notebook generates `preliminary_IPC` as the maximum severity across rCSI, LCS, and FCS indicators:

```python
preliminary_IPC = max(rCSI_IPC, LCS_IPC, FCS_IPC)
```

## Running Analysis Scripts

### Python Environment
```bash
python3 -m pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

### Descriptive Analysis Scripts

**Comprehensive household analysis**:
```bash
python3 src/descriptive_analysis_module/analyze_hha.py
```
Outputs descriptive statistics for variables with <=80% missing values.

**Data structure exploration**:
```bash
python3 src/descriptive_analysis_module/explore_data_structure.py
```
Outputs column inventory, key column checks, and early panel structure exploration.

**Geographic and temporal panel analysis**:
```bash
python3 src/descriptive_analysis_module/geographic_temporal_analysis.py
```
Outputs panel structure, county/sub-county/ward/livelihood-zone distributions, temporal patterns, geographic-temporal cross-tabs, and Excel exports:
- `output/subcounty_by_yearmonth_unique_households.xlsx`
- `output/ward_by_yearmonth_unique_households.xlsx`

### Jupyter Notebook

**IPC variable generation**:
```bash
jupyter notebook src/IPC_variable/genearte_IPC_variable.ipynb
```
Creates rCSI, `rCSI_IPC`, `LCS_IPC`, FCS, `FCS_IPC`, and `preliminary_IPC`, with bar charts and confusion matrices.

## Important Data Considerations

### Missing Data Patterns
- Most variables have <3% missing values
- Many categorical variables contain blank strings (`""`) representing conditional questions
- Example: Milk production questions only apply to households with livestock
- The dataset contains both complete survey responses and partial records

### Geographic Coverage
- **23 counties** in Kenya's ASAL regions
- Most represented: Marsabit, Turkana, Baringo, Garissa, Kitui, Wajir, Mandera
- Unbalanced panel: household observations vary from 1 to 97 time periods

### Temporal Coverage
- **Years**: 2016-2023 (8 years)
- **Months**: Full year coverage with some variation
- Monthly panel structure with roughly 4,000-4,800 unique households per month in the geographic/temporal analysis

## File Path Conventions

The scripts and notebook currently use Windows Dropbox paths for the source dataset:

```python
PATH = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
```

When running scripts from WSL/Linux, verify the data path exists or convert it to the corresponding mounted path. The dataset is stored in a parent directory outside this repository.

## Context for Analysis

### Population Characteristics
- **35.2%** female-headed households
- **49.4%** of household heads have no formal education
- **29.4%** pastoral livelihoods, 19.5% mixed farming
- **46.2%** rely on casual labor as main income

### Food Security Context
- Over **70%** of households used at least one coping strategy in the past week
- **71.8%** consumed no fruit in the past 7 days
- **52.1%** consumed no meat in the past 7 days
- Heavy reliance on purchased food even in agricultural areas

### Water Access Challenges
- Only **14.2%** have piped water access
- **83.7%** do not treat water before drinking
- Primary sources: rivers (20.3%), boreholes (18.8%), pans/dams (17.3%)

## Spec Kit Notes

The repository contains Spec Kit scaffolding under `.specify/`, including templates and a placeholder constitution. If a feature-specific spec or plan is added later, read the active feature's `spec.md`, `plan.md`, and `tasks.md` before implementing Spec Kit tasks.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
