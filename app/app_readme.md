# Streamlit App Overview

## Structure of the App
- UI layout: sidebar for context + main form for inputs + results view.
- Input mapping: user responses mapped to BRFSS-style encoded features.
- Preprocessing: saved `preprocessor.pkl` applies scaling/encoding.
- Prediction: `xgboost_final.pkl` returns risk probability.
- Explanation: SHAP highlights top risk-increasing and risk-reducing factors.

## Features of the App
- Step-by-step health form with clean sections.
- Risk score with low/medium/high category.
- SHAP-based explanations for transparency.
- Recommendations tailored to the risk level.
- Screening disclaimer for safe usage.
