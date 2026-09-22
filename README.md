# COPT Application Cases for Google Colab

Every [COPT](https://www.cardopt.com/) application case from the Cardinal Operations
documentation site, packaged so it runs in Google Colab with one click. Each notebook
opens with a `pip install coptpy` cell; the bundled free license is size-limited but
covers every case here, so no license file is needed.

Every case below was executed end to end on a bare Colab-like runtime with nothing
but `pip install coptpy`. ✅ runs as is; 🔑 solves only with a licensed COPT
(the model is larger than the free build allows); ⚠️ has a known glitch, noted inline.
The free build caps a MIP at 2000 variables and 2000 constraints, and a pure LP at 10000
of each.

| | Case | Level | Domain | Colab | Source |
|---|---|---|---|---|---|
| ✅ | Assignment Problem | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Assignment_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=288) |
| ✅ | Cutting Stock Problem | basic | Manufacture | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Cutting_Stock_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=286) |
| ✅ | Pooling Problem | basic | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Pooling_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=277) |
| 🔑 | Movie Scheduling | intermediate | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Movie_Scheduling.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=272) |
| ✅ | Job Shop Scheduling Problem | basic | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Job_Shop_Scheduling_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=268) |
| ✅ | Production Planning & Sensitivity Analysis | basic | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Production_Planning_Sensitivity_Analysis.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=264) |
| ✅ | Overseas Oil & Gas Benefit-Production Optimization | advanced | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Overseas_Oil_Gas_Benefit_Production_Optimization/oil_optimization-coding-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=261) |
| 🔑 | Warehouse Network Management Problem | advanced | Supply Chain & Logistics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Warehouse_Network_Management_Problem/Warehouse%20network%20management_coding_en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=256) |
| ✅ | Fresh Produce Pricing & Supply Optimization | basic | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Fresh_Produce_Pricing_Supply_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=258) |
| ✅ | Security Constrained Unit Commitment | basic | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Security_Constrained_Unit_Commitment.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=253) |
| ✅ | Performance Evaluation Problem | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Performance_Evaluation_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=250) |
| 🔑 | Powering a Zero-Carbon Island: Co-optimizing Wind, Solar, and Hydrogen Storage | intermediate | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Powering_a_Zero_Carbon_Island_Co_optimizing_Wind_Solar_and_Hydrogen_Storage/pypsa_example_coding_en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=240) |
| ✅ | Curve fitting Problem | basic | Education & Research | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Curve_fitting_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=224) |
| 🔑 | Protein Folding Problem | basic | Healthcare & Medicine | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Protein_Folding_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=223) |
| ✅ | Farming Planning Problem | intermediate | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Farming_Planning_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=215) |
| ✅ | Set Cover Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Set_Cover_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=214) |
| ✅ | Employee Training Plan | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Employee_Training_Plan.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=213) |
| ✅ | Customer-Store Allocation Problem | basic | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Customer_Store_Allocation_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=212) |
| ✅ | Trajectory Smoothing Optimization | advanced | Automatic Control | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Trajectory_Smoothing_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=211) |
| ✅ | Interconnect Delay Optimization | advanced | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Interconnect_Delay_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=209) |
| ✅ | Binary Classification with Logistic Regression | intermediate | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Binary_Classification_with_Logistic_Regression.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=208) |
| ✅ | 0-1 Knapsack Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/0_1_Knapsack_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=204) |
| 🔑 | ATM Cash Management | advanced | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/ATM_Cash_Management/cash-management-model-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=201) |
| ✅ | Risk Parity model | basic | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Risk_Parity_model/risk-parity-model-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=200) |
| ✅ | Index Tracking Portfolio | basic | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Index_Tracking_Portfolio/index-tracking-basic-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=198) |
| ✅ | Curriculum Scheduling Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Curriculum_Scheduling_Problem/Original%20model%20of%20course%20scheduling%20problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=43) |
| ✅ | 3D Tic-Tac-Toe Game | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/3D_Tic_Tac_Toe_Game.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=54) |
| ✅ | Sudoku Game | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Sudoku_Game/sudoku-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=64) |
| ✅ | Linear Regression | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/Linear_Regression.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=130) |
| ✅ | TSP Problem | intermediate | Transportation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/TSP_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=65) |

### Notes

- **Movie Scheduling** 🔑 — needs a licensed COPT — MIP with 825 constraints x 7222 variables, past the free 2000-variable cap
- **Warehouse Network Management Problem** 🔑 — needs a licensed COPT — MIP with 4127 constraints x 4088 variables
- **Powering a Zero-Carbon Island: Co-optimizing Wind, Solar, and Hydrogen Storage** 🔑 — needs a licensed COPT — LP with 30698 constraints x 24864 variables, past the free 10000 cap
- **Protein Folding Problem** 🔑 — needs a licensed COPT — MIP with 2468 constraints, past the free 2000-constraint cap
- **ATM Cash Management** 🔑 — needs a licensed COPT — MIP with 8518 constraints x 8180 variables

## Rebuilding

`tools/copt_cases.py` scrapes the case list and zips from cardopt.com;
`tools/build_repo.py` unpacks them into `notebooks/` and regenerates this table:

```bash
python tools/copt_cases.py --out _zips --raw
python tools/build_repo.py --repo tztgracious/copt-colab-cases --branch main
```
