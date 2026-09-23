# COPT 应用案例 · COPT Application Cases

Cardinal Operations [COPT](https://www.cardopt.com/) 官网的全部应用案例，
改造成开箱即跑的 notebook。每本开头有一格 `pip install coptpy`，
内置的免费许可有规模上限（MIP 2000 变量 / 2000 约束，纯 LP 各 10000），
不需要许可文件。

All application cases from the COPT documentation site, packaged to run with one click.

---

## 中文版 · ModelWhale

国内访问请用 Gitee 镜像。在 ModelWhale 新建项目后，打开 Terminal 执行：

```bash
git clone --depth 1 https://gitee.com/tztgracious/copt-colab-cases.git /tmp/r \
  && CASE=Assignment_Problem \
  && { [ -d /tmp/r/notebooks/zh/$CASE ] && cp -a /tmp/r/notebooks/zh/$CASE/. ~/project/ \
       || cp /tmp/r/notebooks/zh/$CASE.ipynb ~/project/; }
```

把 `CASE` 换成下表的目录名即可。

| | 案例 | 难度 | 领域 | 目录名 | 官网 |
|---|---|---|---|---|---|
| ✅ | 指派问题 | basic | PersonnelPlan | `Assignment_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=288) |
| ✅ | 木材切割问题 | basic | Manufacture | `Cutting_Stock_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=286) |
| ✅ | 汇池问题 | basic | EnergyAndElectricity | `Pooling_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=277) |
| 🔑 | 影院排片优化 | intermediate | SupplyChainManagemen | `Movie_Scheduling` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=272) |
| ✅ | 车间作业调度问题 | basic | ProductionPlan | `Job_Shop_Scheduling_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=268) |
| ✅ | 生产计划与灵敏度分析 | basic | ProductionPlan | `Production_Planning_Sensitivity_Analysis` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=264) |
| ✅ | 海外油气效益产量优化问题 | advanced | EnergyAndElectricity | `Overseas_Oil_Gas_Benefit_Production_Optimization` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=261) |
| 🔑 | 仓网布局问题 | advanced | Supply Chain & Logistics | `Warehouse_Network_Management_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=256) |
| ✅ | 生鲜定价与供应决策优化问题 | basic | SupplyChainManagemen | `Fresh_Produce_Pricing_Supply_Optimization` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=258) |
| ✅ | 安全约束机组组合问题 | basic | EnergyAndElectricity | `Security_Constrained_Unit_Commitment` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=253) |
| ✅ | 绩效评估问题 | basic | PersonnelPlan | `Performance_Evaluation_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=250) |
| 🔑 | 零碳孤岛的风光储氢协同优化 | intermediate | EnergyAndElectricity | `Powering_a_Zero_Carbon_Island_Co_optimizing_Wind_Solar_and_Hydrogen_Storage` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=240) |
| ✅ | 曲线拟合问题 | basic | Education & Research | `Curve_fitting_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=224) |
| 🔑 | 蛋白质氨基酸链折叠问题 | basic | Healthcare & Medicine | `Protein_Folding_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=223) |
| ✅ | 农田轮播排产问题 | intermediate | ProductionPlan | `Farming_Planning_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=215) |
| ✅ | 集合覆盖问题 | basic | Education | `Set_Cover_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=214) |
| ✅ | 人员培训计划 | basic | PersonnelPlan | `Employee_Training_Plan` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=213) |
| ✅ | 客户门店分配问题 | basic | SupplyChainManagemen | `Customer_Store_Allocation_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=212) |
| ✅ | 轨迹平滑优化 | advanced | Automatic Control | `Trajectory_Smoothing_Optimization` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=211) |
| ✅ | 电路互连延迟优化 | advanced | ProductionPlan | `Interconnect_Delay_Optimization` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=209) |
| ✅ | 二分类逻辑回归 | intermediate | Education | `Binary_Classification_with_Logistic_Regression` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=208) |
| ✅ | 0-1背包问题 | basic | Education | `0_1_Knapsack_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=204) |
| 🔑 | 自动取款机现金管理模型 | advanced | Finance | `ATM_Cash_Management` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=201) |
| ✅ | 风险平价模型 | basic | Finance | `Risk_Parity_model` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=200) |
| ✅ | 指数追踪投资组合 | basic | Finance | `Index_Tracking_Portfolio` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=198) |
| ✅ | 选课问题 | basic | Education | `Curriculum_Scheduling_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=43) |
| ✅ | 三维井字棋游戏 | basic | Education | `3D_Tic_Tac_Toe_Game` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=54) |
| ✅ | 数独游戏 | basic | Education | `Sudoku_Game` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=64) |
| ✅ | 线性回归 | basic | Education | `Linear_Regression` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=130) |
| ✅ | 旅行商问题 | intermediate | Transportation | `TSP_Problem` | [文档](https://www.cardopt.com/copt-document/detail?docType=4&id=65) |

---

## English · Google Colab

Every case was executed end to end on a bare runtime with nothing but
`pip install coptpy`. ✅ runs as is; 🔑 solves only with a licensed COPT
(the model is larger than the free build allows); ⚠️ has a known glitch.

| | Case | Level | Domain | Colab | Source |
|---|---|---|---|---|---|
| ✅ | Assignment Problem | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Assignment_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=288) |
| ✅ | Cutting Stock Problem | basic | Manufacture | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Cutting_Stock_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=286) |
| ✅ | Pooling Problem | basic | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Pooling_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=277) |
| 🔑 | Movie Scheduling | intermediate | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Movie_Scheduling.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=272) |
| ✅ | Job Shop Scheduling Problem | basic | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Job_Shop_Scheduling_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=268) |
| ✅ | Production Planning & Sensitivity Analysis | basic | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Production_Planning_Sensitivity_Analysis.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=264) |
| ✅ | Overseas Oil & Gas Benefit-Production Optimization | advanced | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Overseas_Oil_Gas_Benefit_Production_Optimization/oil_optimization-coding-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=261) |
| 🔑 | Warehouse Network Management Problem | advanced | Supply Chain & Logistics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Warehouse_Network_Management_Problem/Warehouse%20network%20management_coding_en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=256) |
| ✅ | Fresh Produce Pricing & Supply Optimization | basic | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Fresh_Produce_Pricing_Supply_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=258) |
| ✅ | Security Constrained Unit Commitment | basic | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Security_Constrained_Unit_Commitment.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=253) |
| ✅ | Performance Evaluation Problem | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Performance_Evaluation_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=250) |
| 🔑 | Powering a Zero-Carbon Island: Co-optimizing Wind, Solar, and Hydrogen Storage | intermediate | EnergyAndElectricity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Powering_a_Zero_Carbon_Island_Co_optimizing_Wind_Solar_and_Hydrogen_Storage/pypsa_example_coding_en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=240) |
| ✅ | Curve fitting Problem | basic | Education & Research | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Curve_fitting_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=224) |
| 🔑 | Protein Folding Problem | basic | Healthcare & Medicine | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Protein_Folding_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=223) |
| ✅ | Farming Planning Problem | intermediate | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Farming_Planning_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=215) |
| ✅ | Set Cover Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Set_Cover_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=214) |
| ✅ | Employee Training Plan | basic | PersonnelPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Employee_Training_Plan.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=213) |
| ✅ | Customer-Store Allocation Problem | basic | SupplyChainManagemen | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Customer_Store_Allocation_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=212) |
| ✅ | Trajectory Smoothing Optimization | advanced | Automatic Control | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Trajectory_Smoothing_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=211) |
| ✅ | Interconnect Delay Optimization | advanced | ProductionPlan | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Interconnect_Delay_Optimization.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=209) |
| ✅ | Binary Classification with Logistic Regression | intermediate | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Binary_Classification_with_Logistic_Regression.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=208) |
| ✅ | 0-1 Knapsack Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/0_1_Knapsack_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=204) |
| 🔑 | ATM Cash Management | advanced | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/ATM_Cash_Management/cash-management-model-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=201) |
| ✅ | Risk Parity model | basic | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Risk_Parity_model/risk-parity-model-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=200) |
| ✅ | Index Tracking Portfolio | basic | Finance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Index_Tracking_Portfolio/index-tracking-basic-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=198) |
| ✅ | Curriculum Scheduling Problem | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Curriculum_Scheduling_Problem/Original%20model%20of%20course%20scheduling%20problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=43) |
| ✅ | 3D Tic-Tac-Toe Game | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/3D_Tic_Tac_Toe_Game.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=54) |
| ✅ | Sudoku Game | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Sudoku_Game/sudoku-en.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=64) |
| ✅ | Linear Regression | basic | Education | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/Linear_Regression.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=130) |
| ✅ | TSP Problem | intermediate | Transportation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tztgracious/copt-colab-cases/blob/main/notebooks/en/TSP_Problem.ipynb) | [doc](https://www.cardopt.com/copt-document/detail?docType=4&id=65) |

### Notes

- **Movie Scheduling** 🔑 — needs a licensed COPT — MIP with 825 constraints x 7222 variables, past the free 2000-variable cap
- **Warehouse Network Management Problem** 🔑 — needs a licensed COPT — MIP with 4127 constraints x 4088 variables
- **Powering a Zero-Carbon Island: Co-optimizing Wind, Solar, and Hydrogen Storage** 🔑 — needs a licensed COPT — LP with 30698 constraints x 24864 variables, past the free 10000 cap
- **Protein Folding Problem** 🔑 — needs a licensed COPT — MIP with 2468 constraints, past the free 2000-constraint cap
- **ATM Cash Management** 🔑 — needs a licensed COPT — MIP with 8518 constraints x 8180 variables

---

## Rebuilding

```bash
python tools/copt_cases.py --out _zips --lang en
python tools/copt_cases.py --out _zips_zh --lang zh
python tools/build_repo.py --repo tztgracious/copt-colab-cases --branch main
```
