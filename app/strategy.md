## app.py structure
1. imports + model loading 
2. page config
3. title + description
4. input form (sidebar or main)
5. prediction button
6. results display
7. SHAP explanation
8. recommendations

## Input Sections: 
- Section 1 — About You (demographics)
→ age, sex, income, education

- Section 2 — Your Body (biometrics)  
→ height, weight (BMI calculated automatically)

- Section 3 — Lifestyle
→ smoking status, alcohol, exercise

- Section 4 — How You Feel (recent health)
→ general health rating, physical health days, mental health days

- Section 5 — Medical History
→ heart attack, coronary disease, stroke, kidney disease, 
  arthritis, depression, cancer, asthma, HIV test

- Section 6 — Healthcare Access
→ insurance, personal doctor, last checkup, avoided doctor due to cost

## Input Strategy
ask user directly (plain english questions):

SEX → "What is your biological sex?" ✅
_AGEG5YR → "What is your age?" (then map to band) ✅
_BMI5 → calculate from height + weight input ✅
INCOME2 → "What is your annual household income?" (dropdown) ✅
EDUCA → "What is your highest education level?" (dropdown) ✅
GENHLTH → "How would you rate your general health?" (1-5 scale) ✅
PHYSHLTH → "In the past 30 days, how many days was your physical health not good?" ✅
MENTHLTH → "In the past 30 days, how many days was your mental health not good?"✅
EXERANY2 → "Did you exercise in the past 30 days?" (yes/no) ✅
DRNKANY5 → "Have you had any alcohol in the past 30 days?" (yes/no) ✅
ALCDAY5 → "How many days did you drink alcohol in the past 30 days?" ✅
_SMOKER3 → "What is your smoking status?" (current/former/never) ✅
_CHLDCNT → "How many children are in your household?" ✅
HLTHPLN1 → "Do you have health insurance?" (yes/no)  
MEDCOST → "In the past year, did you avoid doctor due to cost?" (yes/no)
PERSDOC2 → "Do you have a personal doctor?" (yes/no)
CHECKUP1 → "When was your last routine checkup?" (dropdown)

medical history (yes/no questions):

CVDINFR4 → "Have you ever had a heart attack?"
CVDCRHD4 → "Have you ever had coronary heart disease?"

CVDSTRK3 → "Have you ever had a stroke?"

CHCKIDNY → "Have you ever had kidney disease?"

HAVARTH3 → "Have you ever had arthritis?"
_DRDXAR1 → "Have you ever been diagnosed with arthritis by a doctor?"

ADDEPEV2 → "Have you ever had depression?"

CHCOCNCR → "Have you ever had skin cancer?"
CHCSCNCR → "Have you ever had any other cancer?"

_ASTHMS1 → "What is your asthma status?" (never/former/current)

HIVTST6 → "Have you ever been tested for HIV?"

calculated/derived:

_RFBING5 → calculate from alcohol inputs
_RFHLTH → derive from GENHLTH input
_HCVU651 → derive from age + insurance status
_TOTINDA → derive from EXERANY2
QLACTLM2 → "Are you limited in activities due to health?" (yes/no) — ask directly
_AIDTST3 → same as HIVTST6 — derive directly