# Project Context for Claude Code

## Project
AI-Powered Early Disease Risk Prediction & Explainable Health Intelligence System

## Goal
End-to-end ML/DL project for internship preparation. Predicts diabetes risk using the 
CDC BRFSS dataset (2011-2015) from Kaggle.

## Mentor Style
- Act as a senior data science mentor
- Guide step by step — do NOT give full solutions unless explicitly asked
- Ask interview-style questions to check understanding
- Suggest best practices and industry norms
- Help debug approach, not just code

## Current Status
Week 4, Day 9 — COMPLETED ✅
Week 5, Day 10 — Starting next (Deep Learning begins)

## Completed So Far
- [x] Project folder structure created
- [x] Raw dataset downloaded and placed in data/raw/
- [x] problem_statement.md written
- [x] README.md created
- [x] CLAUDE.md context file created
- [x] First GitHub commit pushed
- [x] All 5 CSVs loaded and inspected
- [x] Common columns identified (157)
- [x] merged_df created (2.38M rows, 158 cols)
- [x] Survey_year column added
- [x] Target variable (DIABETE3) mapped to binary
- [x] Sentinel values handled throughout
- [x] Feature selection complete (157 → 36 cols)
- [x] Missing values handled (imputation + row dropping)
- [x] EDA complete (univariate, bivariate, correlation)
- [x] Hypothesis testing complete (t-test, chi-square)
- [x] Confidence intervals + Cohen's d calculated
- [x] Probability distributions identified
- [x] Bayes theorem applied
- [x] Binary encoding complete (1/2 → 1/0)
- [x] Final sentinel audit complete
- [x] Train/test split (80/20 stratified)
- [x] Preprocessing pipeline built (StandardScaler, OrdinalEncoder)
- [x] x_train, x_test, y_train, y_test saved to data/processed/
- [x] Logistic Regression trained (ROC-AUC=0.801, recall=0.74)
- [x] Decision Tree trained (ROC-AUC=0.802, recall=0.77)
- [x] Random Forest trained + tuned (ROC-AUC=0.807, recall=0.75)
- [x] KNN trained (ROC-AUC=0.690, recall=0.19) — poor performer
- [x] XGBoost trained + tuned (ROC-AUC=0.813, recall=0.76) — best model
- [x] SVM skipped — computationally infeasible on 2M rows
- [x] Threshold tuning complete — final threshold=0.40
- [x] SMOTE skipped — class_weight='balanced' sufficient at this scale
- [x] Neural network built (TF/Keras) — ROC-AUC=0.807
- [x] ML vs DL comparison complete — XGBoost wins
- [x] All models saved to models/
- [x] SHAP summary + waterfall plots generated
- [x] PNEUVAC3 removed — reverse causality confirmed by SHAP
- [x] XGBoost retrained on 34 features — ROC-AUC=0.808
- [x] Final model saved: models/xgboost_final.pkl

## Dataset
- Final shape: 2,018,571 rows, 36 cols
- Train: 1,614,856 rows
- Test: 403,715 rows
- Class balance: 84% no diabetes, 16% diabetes

## Best Model So Far
- XGBoost (tuned)
- ROC-AUC: 0.813
- Recall class 1: 0.76 (threshold=0.5) / 0.85 (threshold=0.40)
- Precision class 1: 0.32 (threshold=0.5) / 0.28 (threshold=0.40)
- Best params: learning_rate=0.12, max_depth=4, n_estimators=120
- Final threshold: 0.40 (screening tool context)

## Feature Sets
- Binary (23): _RFBING5, _AIDTST3, HLTHPLN1, QLACTLM2, CHCOCNCR,
  _RFHLTH, HAVARTH3, HIVTST6, MEDCOST, CHCSCNCR, EXERANY2, DRNKANY5,
  _HCVU651, ADDEPEV2, PERSDOC2, CVDSTRK3, _TOTINDA, CHCKIDNY,
  CVDCRHD4, CVDINFR4, SEX, _DRDXAR1, PNEUVAC3
- Continuous (3): PHYSHLTH, _BMI5, ALCDAY5
- Ordinal (9): _SMOKER3, GENHLTH, MENTHLTH, _AGEG5YR, INCOME2,
  EDUCA, _ASTHMS1, CHECKUP1, _CHLDCNT

## Model Comparison Summary
| Model | ROC-AUC | Recall (class 1) | Notes |
|---|---|---|---|
| Logistic Regression | 0.801 | 0.74 | Good baseline |
| Decision Tree | 0.802 | 0.77 | Simple, interpretable |
| Random Forest (tuned) | 0.807 | 0.75 | Ensemble, robust |
| KNN | 0.690 | 0.19 | Poor — subsample + imbalance |
| XGBoost (tuned) | 0.813 | 0.76 | Best performer |
| SVM | N/A | N/A | Skipped — too slow |

## Key Design Decisions
- Binary classification (diabetic: yes/no)
- Dataset size justifies deep learning
- Healthcare context — False Negatives more costly than False Positives
- Class imbalance handled via class_weight='balanced' + threshold tuning
- Evaluation priority: ROC-AUC, Recall, F1 over plain accuracy
- Final threshold=0.40 chosen for screening tool context
- Precision ceiling ~0.28-0.32 due to 84/16 class imbalance — documented limitation

## 8-Week Roadmap
- Week 1: Problem definition + data collection ✅
- Week 2: EDA + statistical analysis ✅
- Week 3: Feature engineering + preprocessing pipeline ✅
- Week 4: Train and compare ML models ✅
- Week 5: Deep learning model ← NEXT
- Week 6: Explainable AI + error analysis
- Week 7: Web app (Streamlit or Flask)
- Week 8: Final polish + documentation