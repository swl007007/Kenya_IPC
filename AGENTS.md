# Repository Guidelines

## Project Structure & Module Organization
This repository contains Python and notebook-based food security analysis for Kenya ASAL household survey data. Source scripts live in `src/`. Use `src/descriptive_analysis_module/` for reusable exploratory and geographic-temporal analyses, and `src/IPC_variable/genearte_IPC_variable.ipynb` for IPC indicator generation. Reports belong in `doc/`; generated charts, CSVs, and Excel workbooks belong in `output/`. The main Stata dataset, `HHA_all.dta`, is stored outside the repository, so do not assume it is committed.

## Build, Test, and Development Commands
Install the working Python stack before running analyses:

```bash
python3 -m pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

Run the main scripts from the repository root:

```bash
python3 src/descriptive_analysis_module/analyze_hha.py
python3 src/descriptive_analysis_module/explore_data_structure.py
python3 src/descriptive_analysis_module/geographic_temporal_analysis.py
jupyter notebook src/IPC_variable/genearte_IPC_variable.ipynb
```

The scripts use a Windows Dropbox path for `HHA_all.dta`; when running from WSL/Linux, convert it to the mounted path or update the local variable before execution.

## Coding Style & Naming Conventions
Use Python 3 with 4-space indentation. Keep analysis functions named in lowercase with underscores, for example `analyze_panel` or `analyze_stata_file`. Prefer descriptive variable names that match dataset columns (`county`, `subcounty`, `livelihoodzone`) rather than positional aliases unless exploring raw structure. Keep output filenames explicit about geography, time, and metric, such as `ward_by_yearmonth_unique_households.xlsx`.

## Testing Guidelines
There is no formal test suite in this repository. Validate changes by running the affected script or notebook end to end and checking regenerated artifacts in `output/`. For data transformations, compare row counts, year/month coverage, key category levels, and IPC phase distributions before and after edits.

## Commit & Pull Request Guidelines
Recent commits use short, direct summaries such as `minor workbook change` and `update 2025data remove pilot data`. Keep commit messages concise and scoped to the changed analysis or artifact. Pull requests should describe the data path used, commands run, outputs regenerated, and any expected changes in tables or figures. Include screenshots only when chart appearance changed.

## Security & Configuration Tips
Do not commit raw household data or local Dropbox paths beyond script defaults already present. Treat generated reports as potentially sensitive if they expose small geographic groups or household counts.
