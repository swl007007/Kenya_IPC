# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project analyzing household survey data from Kenya's Arid and Semi-Arid Lands (ASAL) regions. The project focuses on food security analysis using the Integrated Food Security Phase Classification (IPC) methodology.

**Primary Dataset**: `HHA_all.dta` - A longitudinal panel dataset covering 375,959 household observations across 23 counties in Kenya from 2016-2023.

**Key Research Goals**:
- Analyze household food security indicators (rCSI - reduced Coping Strategy Index, LCS - Livelihood Coping Strategies)
- Generate IPC preliminary classifications based on household coping strategies
- Conduct geographic and temporal analysis of food security patterns

## Repository Structure

```
Kenya_IPC/
├── src/
│   ├── descriptive_analysis_module/    # Exploratory analysis scripts
│   │   ├── analyze_hha.py             # Comprehensive descriptive statistics
│   │   ├── analyze_geographic_temporal.py  # Geographic/temporal distribution
│   │   ├── geographic_temporal_analysis.py # Enhanced panel analysis
│   │   └── explore_data_structure.py  # Dataset structure exploration
│   └── IPC_variable/
│       └── genearte_IPC_variable.ipynb # IPC variable calculation notebook
├── doc/                               # Analysis outputs and documentation
│   ├── Geographic_Temporal.txt       # Geographic/temporal analysis report
│   └── HHA_all_other_descriptive_analysis.md  # Comprehensive analysis report
└── output/                           # Generated visualizations
    ├── IPC_preliminary.png
    ├── LCS_IPC.png
    ├── rCSI_IPC.png
    └── rCSI_LCS_confusion_matrix.png
```

## Data Structure

### Dataset: HHA_all.dta

**Panel Structure**:
- **Household ID**: `qid` or `householdcode`
- **Time dimensions**: `year` (2016-2023), `month` (monthly observations)
- **Geographic hierarchy**: `county` → `subcounty` → `ward`
- **Livelihood zones**: `livelihoodzone` (Pastoral, Mixed Farming, Agro Pastoral, etc.)

**Column names**: The dataset uses descriptive column names:
- `county` - County name
- `subcounty` - Sub-county name
- `ward` - Ward name
- `livelihoodzone` - Livelihood zone classification
- `month` - Month name (January, February, etc.)
- `year` - Year (2016-2023)
- `householdcode`, `qid` - Household identifiers

### Key Variable Categories

**Coping Strategy Index (CSI) variables**:
- Consumption-based: `csi_reliedonless`, `csi_borrowedfood`, `csi_reducednoofmeals`, `csi_reducedportionmealsize`, `csi_quantityforadult`
- Livelihood-based: `csi_soldhouseholdassets`, `csi_soldproductiveassets`, `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldhouseland`, `csi_withdrewchildrenschool`, `csi_soldlastfemaleanimal`, `csi_begging`, `csi_soldmoreanimals`

**Food consumption variables**: `hfc_*` (days consumed in past 7 days and source)

**Water access variables**: `watersource*`, `normalwatersource`, `distancefromwatersource`, `hhpayforwater`

## IPC Calculation Methodology

### rCSI (reduced Coping Strategy Index)
```python
rCSI = (1 × csi_reliedonless +
        2 × csi_borrowedfood +
        1 × csi_reducednoofmeals +
        1 × csi_reducedportionmealsize +
        3 × csi_quantityforadult)
```

**IPC Classification from rCSI**:
- Phase 1 (Minimal): rCSI 0-3
- Phase 2 (Stressed): rCSI 4-18
- Phase 3 (Crisis+): rCSI ≥19

### LCS_IPC (Livelihood Coping Strategies)
Classify household coping strategies into severity levels:
- **Phase 1 (Minimal)**: No significant coping (value = 0, recoded to 1)
- **Phase 2 (Stress)**: `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldmoreanimals` (recoded to 2)
- **Phase 3 (Crisis)**: `csi_soldhouseholdassets`, `csi_reducednonfoodexpenses`, `csi_soldproductiveassets`, `csi_withdrewchildrenschool` (recoded to 3)
- **Phase 4 (Emergency)**: `csi_soldhouseland`, `csi_soldlastfemaleanimal`, `csi_begging` (recoded to 4)

LCS_IPC is the **maximum** severity across all livelihood coping strategies.

### IPC_preliminary
```python
IPC_preliminary = max(rCSI_IPC, LCS_IPC)
```

## Running Analysis Scripts

### Python Environment
```bash
# The scripts use Python 3 with pandas, numpy, matplotlib, seaborn
python3 -m pip install pandas numpy matplotlib seaborn
```

### Descriptive Analysis Scripts

**Comprehensive household analysis**:
```bash
python3 src/descriptive_analysis_module/analyze_hha.py
```
Outputs: Descriptive statistics for all variables with ≤80% missing values

**Geographic and temporal distribution**:
```bash
python3 src/descriptive_analysis_module/analyze_geographic_temporal.py
```
Outputs: Panel structure, county/ward/livelihood zone distributions, temporal patterns

**Data structure exploration**:
```bash
python3 src/descriptive_analysis_module/explore_data_structure.py
```
Outputs: Column inventory and panel identifiers

### Jupyter Notebook

**IPC variable generation**:
```bash
jupyter notebook src/IPC_variable/genearte_IPC_variable.ipynb
```
Creates rCSI, rCSI_IPC, LCS_IPC, and IPC_preliminary variables with visualizations

## Important Data Considerations

### Missing Data Patterns
- Most variables have <3% missing values
- Many categorical variables contain blank strings (`""`) representing conditional questions
- Example: Milk production questions only apply to households with livestock
- The dataset contains both complete survey responses (~9,419 households) and partial records

### Geographic Coverage
- **23 counties** in Kenya's ASAL regions
- Most represented: Marsabit, Turkana, Baringo, Garissa, Kitui, Wajir, Mandera
- Unbalanced panel: household observations vary from 1 to 97 time periods

### Temporal Coverage
- **Years**: 2016-2023 (8 years)
- **Months**: Full year coverage with some variation
- Monthly panel structure with ~4,000-4,800 unique households per month

## File Path Conventions

**Data paths**: The scripts currently use Windows paths pointing to Dropbox:
```python
PATH = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
```

When running scripts, verify the data file path matches your environment. The dataset is stored in a parent directory outside this repository.

## Context for Analysis

### Population Characteristics
- **35.2%** female-headed households
- **49.4%** of household heads have no formal education
- **29.4%** pastoral livelihoods, 19.5% mixed farming
- **46.2%** rely on casual labor as main income (highly vulnerable)

### Food Security Context
- Over **70%** of households used at least one coping strategy in past week
- **71.8%** consumed no fruit in past 7 days
- **52.1%** consumed no meat in past 7 days
- Heavy reliance on purchased food even in agricultural areas

### Water Access Challenges
- Only **14.2%** have piped water access
- **83.7%** do not treat water before drinking
- Primary sources: rivers (20.3%), boreholes (18.8%), pans/dams (17.3%)
