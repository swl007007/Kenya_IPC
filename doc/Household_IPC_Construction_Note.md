# Household IPC Construction Note for Kenya HHA Data

## Purpose

This note documents how `src/IPC_variable/genearte_IPC_variable.ipynb` constructs household-level preliminary IPC phases for Kenya household survey records and how those household phases are aggregated to ward and sub-county area phases. The phase-convergence matrix used to produce the household preliminary/overall phase is from the local FEWS NET matrix-analysis reference, `C:\Users\WeilunShi\IFPRI Dropbox\Weilun Shi\Google fund\literature\Topic1\FEWSNET_matrix_analysis.pdf` (available in this environment as `/mnt/c/Users/swl00/IFPRI Dropbox/Weilun Shi/Google fund/literature/Topic1/FEWSNET_matrix_analysis.pdf`). The workflow is compatible with the FEWS NET/IPC acute food insecurity framework because it uses the same core evidence families: food consumption, consumption coping, and livelihood coping. It should be read as a transparent analytical approximation, not as an official IPC classification, because official IPC analysis also requires expert convergence, reliability review, contextual evidence, and, where relevant, nutrition, mortality, and humanitarian assistance analysis.

## Reference Framework

The immediate source for the notebook's phase-convergence matrix is `FEWSNET_matrix_analysis.pdf`. The IPC Technical Manual Version 3.1 is the broader reference framework used to explain why that matrix is FEWS NET/IPC-compatible. FEWS NET is one of the IPC Global Partners listed in the manual, so using IPC Acute Food Insecurity phase logic is the appropriate way to align this household classification with FEWS NET-compatible analysis. The IPC manual defines five acute food insecurity phases: Phase 1 None/Minimal, Phase 2 Stressed, Phase 3 Crisis, Phase 4 Emergency, and Phase 5 Catastrophe/Famine. The notebook uses Phases 1 to 4 because the household survey indicators used here are rCSI, FCS, and LCS; the workflow does not attempt to identify Phase 5 Catastrophe/Famine, which requires stronger evidence on extreme food gaps and other conditions.

The IPC acute food insecurity framework treats food consumption and livelihood change as first-level outcomes. It also states that reference-table thresholds should guide convergence of evidence, while recognizing that indicators need contextual interpretation. The notebook operationalizes the FEWS NET matrix reference with a deterministic two-stage matrix: first a food-consumption severity is derived from rCSI and FCS, then livelihood coping adjusts the final preliminary household phase.

## Input Data

The notebook reads:

```python
PATH = r"C:\Users\swl00\IFPRI Dropbox\Weilun Shi\Kenya-MUAC data\Processed_data\HHA_all.dta"
data = pd.read_stata(PATH)
```

The relevant fields are:

- Consumption coping variables: `csi_reliedonless`, `csi_borrowedfood`, `csi_reducednoofmeals`, `csi_reducedportionmealsize`, `csi_quantityforadult`.
- Livelihood coping variables: `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldmoreanimals`, `csi_soldhouseholdassets`, `csi_reducednonfoodexpenses`, `csi_soldproductiveassets`, `csi_withdrewchildrenschool`, `csi_soldhouseland`, `csi_soldlastfemaleanimal`, `csi_begging`.
- Food consumption variables: grain/root, pulse, milk, meat/fish/egg, vegetable, fruit, oil, sugar, and condiment consumption day variables.
- Aggregation keys: `ward`, `subcounty`, `month`, and `year`.

## Step 1: Reduced Coping Strategies Index

The notebook first converts all `csi_` fields to numeric values. It then computes the reduced Coping Strategies Index:

```python
rCSI =
    1 * csi_reliedonless
  + 2 * csi_borrowedfood
  + 1 * csi_reducednoofmeals
  + 1 * csi_reducedportionmealsize
  + 3 * csi_quantityforadult
```

This follows the standard rCSI weighting logic: relying on less preferred food, reducing meals, and reducing portions receive weight 1; borrowing food receives weight 2; restricting adult consumption receives weight 3.

The notebook maps rCSI to IPC-style severity:

| rCSI range | Notebook variable | Phase meaning |
| --- | --- | --- |
| 0-3 | `rCSI_IPC = 1` | None/Minimal |
| 4-18 | `rCSI_IPC = 2` | Stressed |
| >=19 | `rCSI_IPC = 3` | Crisis or worse signal |

This matches the IPC reference-table use of rCSI: 0-3 for Phase 1, 4-18 for Phase 2, and >=19 as a Phase 3+ signal. The manual treats rCSI >=19 as non-defining for differentiating Phases 3, 4, and 5, so the notebook correctly does not use rCSI alone to assign Phase 4.

## Step 2: Livelihood Coping Strategies

The notebook recodes the livelihood coping variables so that the relevant response values are converted to binary use indicators. It then assigns each strategy to an IPC-compatible severity group:

| Severity group | Notebook phase value | Variables |
| --- | --- | --- |
| Stress coping | 2 | `csi_spentsavings`, `csi_borrowedmoney`, `csi_soldmoreanimals` |
| Crisis coping | 3 | `csi_soldhouseholdassets`, `csi_reducednonfoodexpenses`, `csi_soldproductiveassets`, `csi_withdrewchildrenschool` |
| Emergency coping | 4 | `csi_soldhouseland`, `csi_soldlastfemaleanimal`, `csi_begging` |

`LCS_IPC` is the maximum severity among the livelihood coping strategies used by the household. If none of the listed stress, crisis, or emergency strategies is observed, the notebook recodes `0` to `1`, meaning no stress/crisis/emergency livelihood coping observed.

This follows the IPC reference-table logic for LCS: stress strategies indicate Phase 2 livelihood stress, crisis strategies indicate Phase 3 accelerated depletion or erosion of assets, and emergency strategies indicate Phase 4 extreme depletion or liquidation of assets.

## Step 3: Food Consumption Score

The notebook constructs WFP-style food groups from reported food-consumption days:

| Food group | Notebook construction | Weight |
| --- | --- | --- |
| Staples | max(`hfc_graindays`, `hfc_rootsdays`) | 2 |
| Pulses/nuts | `hfc_pulsesnutsdays` | 3 |
| Dairy | `hfc_milkdays` | 4 |
| Protein | max(`hfc_meatdays`, `hfc_liverdays`, `hfc_fishdays`, `hfc_eggsdays`) | 4 |
| Vegetables | max(`hfc_orangevegdays`, `hfc_greenleafydays`, `hfc_othervegdays`) | 1 |
| Fruits | max(`hfc_orangefruitsdays`, `hfc_otherfruitsdays`) | 1 |
| Fat | `hfc_oildays` | 0.5 |
| Sugar | `hfc_sugardays` | 0.5 |

The resulting formula is:

```python
FCS =
    FCSStap * 2
  + FCSPulse * 3
  + FCSDairy * 4
  + FCSPr * 4
  + FCSVeg * 1
  + FCSFruits * 1
  + FCSFat * 0.5
  + FCSSugar * 0.5
```

Condiments are recorded as `FCSCond` but are not included in the score formula, which is consistent with the standard FCS approach.

The notebook maps FCS to severity:

| FCS range | Notebook variable | IPC-compatible interpretation |
| --- | --- | --- |
| >35 | `FCS_IPC = 1` | Acceptable food consumption |
| >21 and <=35 | `FCS_IPC = 3` | Borderline food consumption |
| <=21 | `FCS_IPC = 4` | Poor food consumption |

The IPC manual identifies FCS as a WFP corporate indicator based on nine food groups, seven-day consumption frequency, and nutritional weights. It also states that poor, borderline, and acceptable FCS groupings are used as cutoffs in the IPC Acute Food Insecurity Reference Table.

## Step 4: Household Food IPC Matrix

The notebook does not classify households by taking the maximum of rCSI, FCS, and LCS. Instead, it uses the two-stage matrix from `FEWSNET_matrix_analysis.pdf`.

First, it combines `rCSI_IPC` and `FCS_IPC` into `Food_IPC`:

| rCSI_IPC | FCS_IPC | Food_IPC |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 3 | 1 |
| 1 | 4 | 2 |
| 2 | 1 | 2 |
| 2 | 3 | 2 |
| 2 | 4 | 3 |
| 3 | 1 | 3 |
| 3 | 3 | 3 |
| 3 | 4 | 4 |

This matrix is more nuanced than a maximum rule. For example, acceptable rCSI with borderline FCS remains `Food_IPC = 1`, while acceptable rCSI with poor FCS becomes `Food_IPC = 2`. High rCSI, even with acceptable FCS, is treated as `Food_IPC = 3`, because severe consumption coping is evidence that the household is protecting consumption through stressed behavior.

## Step 5: Preliminary Household IPC Matrix

Second, following the same FEWS NET matrix reference, the notebook combines `Food_IPC` with `LCS_IPC`:

| Food_IPC | LCS_IPC | preliminary_IPC |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 2 | 1 |
| 1 | 3 | 2 |
| 1 | 4 | 3 |
| 2 | 1 | 2 |
| 2 | 2 | 2 |
| 2 | 3 | 3 |
| 2 | 4 | 3 |
| 3 | 1 | 3 |
| 3 | 2 | 3 |
| 3 | 3 | 3 |
| 3 | 4 | 4 |
| 4 | any | 4 |

This implements the IPC concept that households can appear food-secure in current consumption but still be in a worse food-security phase if they are only maintaining consumption by damaging livelihoods. Crisis livelihood coping can move a household from Phase 1 food consumption to Phase 2, and emergency coping can move it to Phase 3. When the food-consumption evidence is already Phase 4, the household remains Phase 4 regardless of LCS.

## Step 6: Ward and Sub-county Area Classification

After assigning `preliminary_IPC` to households, the notebook aggregates counts by:

- `ward`, `month`, `year`
- `subcounty`, `month`, `year`

For each area-month, it computes household counts and percentages in Phase 1, Phase 2, Phase 3, and Phase 4. It then assigns `overall_phase` using a cascading 20 percent threshold:

```python
if Phase4_Percentage >= 20:
    overall_phase = 4
elif Phase3_Percentage >= 20:
    overall_phase = 3
elif Phase2_Percentage >= 20:
    overall_phase = 2
elif Phase1_Percentage >= 20:
    overall_phase = 1
else:
    overall_phase = 0
```

This mirrors the IPC area-classification rule: an area is classified in the most severe phase affecting at least 20 percent of the population. The notebook exports these area-level outputs to:

- `output/ward_level.csv`
- `output/sub_county_level.csv`

It also defines ward-level food crisis as:

```python
food_crisis = overall_phase >= 3
```

This is consistent with FEWS NET/IPC reporting conventions that commonly summarize Crisis or worse as Phase 3+.

## Why This Is FEWS NET/IPC-Compatible

The workflow is FEWS NET/IPC-compatible for four reasons.

First, it uses the IPC Acute Food Insecurity phase scale and labels: None/Minimal, Stressed, Crisis, and Emergency. It avoids assigning Phase 5 because the available indicators are insufficient for a formal Catastrophe/Famine classification.

Second, it is built around IPC first-level outcomes. rCSI captures consumption coping, FCS captures food consumption frequency and diversity, and LCS captures livelihood stress and asset depletion.

Third, it implements the FEWS NET matrix-analysis document's household convergence logic using internationally recognized indicator cutoffs reflected in the IPC manual: rCSI 0-3, 4-18, and >=19; FCS poor, borderline, and acceptable groups; and LCS stress, crisis, and emergency groupings.

Fourth, it applies the IPC 20 percent rule when moving from household records to area phases. The area is not classified by the single worst household, nor by an average phase. It is classified by whether at least 20 percent of households are in a given phase, checked from the most severe phase downward.

## Important Caveats

This notebook produces a preliminary household and area classification. It is not an official IPC product. A formal IPC classification would also require a full convergence-of-evidence process, reliability scoring, documentation of assumptions, nutrition and mortality evidence where relevant, humanitarian assistance treatment, population estimates, and expert consensus. The current notebook is therefore best described as a FEWS NET matrix-based, IPC-compatible household indicator workflow with IPC-style area aggregation.

## Sources

- IPC Global Partners. 2021. [Integrated Food Security Phase Classification Technical Manual Version 3.1](https://www.ipcinfo.org/ipc/technical/manual_en).
- FEWS NET matrix-analysis reference: `C:\Users\WeilunShi\IFPRI Dropbox\Weilun Shi\Google fund\literature\Topic1\FEWSNET_matrix_analysis.pdf`.
- Notebook implementation: `src/IPC_variable/genearte_IPC_variable.ipynb`.
