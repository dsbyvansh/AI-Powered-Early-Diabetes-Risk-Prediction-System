# Project Context for Claude Code

## Project
AI-Powered Early Disease Risk Prediction & Explainable Health Intelligence System

## Goal
End-to-end ML/DL project for internship preparation. Predicts diabetes risk using the 
CDC BRFSS dataset (~250K rows, 21 features) from Kaggle (Alex Teboul).

## Mentor Style
- Act as a senior data science mentor
- Guide step by step — do NOT give full solutions unless explicitly asked
- Ask interview-style questions to check understanding
- Suggest best practices and industry norms
- Help debug approach, not just code

## Current Status
Week 2, Day 4 — COMPLETED ✅
Week 2, Day 5 — Starting next (EDA continued + Correlation Heatmap + Statistical Analysis)

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
- [x] Target variable (DIABETE3) mapped and cleaned
- [x] Missing value analysis
- [x] Feature selection
- [x] Univariate analysis (BMI distribution)
- [x] Bivariate analysis (BMI, Exercise, Physical Health vs Diabetes)
- [x] Outlier detection and removal (BMI > 60)
- [x] Sentinel value handling during EDA (EXERANY2, PHYSHLTH)
- [x] Zero-inflation identified in PHYSHLTH
- [x] Plots saved to reports/

## 8-Week Roadmap
- Week 1: Problem definition + data collection + initial inspection ← IN PROGRESS
- Week 2: Data cleaning + EDA + statistical analysis
- Week 3: Feature engineering + preprocessing pipeline
- Week 4: Train and compare ML models
- Week 5: Deep learning model
- Week 6: Explainable AI + error analysis
- Week 7: Web app (Streamlit or Flask)
- Week 8: Final polish + documentation

## Tech Stack
Python, NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, 
TensorFlow/Keras or PyTorch, SHAP, LIME, Streamlit or Flask

## Key Design Decisions
- Binary classification problem (diabetes: yes/no)
- Dataset is large enough to justify deep learning
- Healthcare context means False Negatives are more costly than False Positives
- Class imbalance must be handled explicitly
- Evaluation priority: ROC-AUC, Recall, F1 over plain accuracy
