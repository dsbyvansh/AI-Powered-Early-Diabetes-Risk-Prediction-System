# AI Powered Disease Risk Prediction

I am going to be predicting the risk of Diabetes and Heart Problems for every age group

The End User of this system will be any person who wants to predict the risk of diabetes or heart problems and fix their lifestyle

## Example data (provided by the end user)
- Personal Data: Name, DOB, Email, Phone number, informal address(country,city,state)
- Health Data:
    - Basic: Age,Gender,Height,Weight,BMI
    - Lifestyle: Smoking status, Alcohol Consumption, Phyisical Activity level, Sleep Quality, Dietary Habits (Super Important)
    - Hereditary: Family Medical History (in diabetes,heart disease,hypertension,high blood sugar,high cholestrol,chest pain)
    - Vitals : Blood Pressure, Resting Heart Rate
    - Diabetes Specific: Insulin Level, HbA1c (very important)
    - Heart Specific: Total Cholestrol, HDL/LDL Cholestrol, Exercise Frequency (Cardio or strength training), Stress Level

## Meaning Of Risk Prediction
- Risk Prediction means predicting the risk category(high,med,low) + causing factors of diabetes or heart disease by looking at several factors (data)
- Risk Factors Like:
    - Age 
    - Weight/BMI 
    - Blood Pressure  
    - Blood Sugar 
    - Cholestrol
    - Family History
    - Lifestyle (Smoking,Exercise,Diet,Sleep,Stres)
    - Chest Pain History
- This problem statement is big enough to consider under both classification and regression

## Confusion Matrix Clarity
- A confusion matrix is a performance measurement tool for machine learning classification algorithms 
- Key Components:
    - True Positive (TP): Correctly predicted positive instance.
    - True Negative (TN): Correctly predicted negative instance.
    - False Positive (FP): Incorrectly predicted positive (Type 1 Error).
    - False Negative (FN): Incorrectly predicted negative (Type 2 Error).
    
A False Negative in this context will mean that the risk predicted by the model is incorrect as compared to the actual risk.
Both FN and FP are equally Harmful in Healthcare as both lead to a sense of stress in the end user , which is why choosing the right model is very crucial.
