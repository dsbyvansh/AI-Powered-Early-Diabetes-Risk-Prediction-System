import streamlit as st
import joblib
import pandas as pd
import shap

if 'page' not in st.session_state:
     st.session_state['page'] = 'form' #default

 
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout='wide'
)
st.markdown("""
    <style>
    [data-testid="stForm"] {
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(128,128,128,0.2);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### About This Tool")
    st.info("""
    This screening tool uses machine learning 
    trained on 2M+ CDC survey responses to 
    estimate diabetes risk.
    
    **Not a medical diagnosis.**
    Always consult a healthcare provider.
    """)
    st.markdown("### How it works")
    st.markdown("""
    1. Fill in your health details
    2. Click **Run Risk Screening**
    3. View your risk score + key factors
    """)

@st.cache_resource
def load_artifacts():
    model = joblib.load('C:/Users/Vansh/Desktop/Project/models/xgboost_final.pkl')
    preprocessor = joblib.load('C:/Users/Vansh/Desktop/Project/models/preprocessor.pkl')
    return model,preprocessor

model,preprocessor = load_artifacts()


def map_to_age_band(age):
    if age < 25: return 1.0
    elif age < 30: return 2.0
    elif age < 35: return 3.0
    elif age < 40: return 4.0
    elif age < 45: return 5.0
    elif age < 50: return 6.0
    elif age < 55: return 7.0
    elif age < 60: return 8.0
    elif age < 65: return 9.0
    elif age < 70: return 10.0
    elif age < 75: return 11.0
    elif age < 80: return 12.0
    elif age < 85: return 13.0
    else: return 14.0 

asthma_mapping = {
    "Never": 1.0,
    "Former": 2.0,
    "Current": 3.0
}

income_mapping = {
    "Less than $15,000": 1.0,   
    "$15,000 - $25,000": 2.0,   
    "$25,000 - $50,000": 4.0,   
    "$50,000 - $75,000": 6.0,   
    "$75,000 or more": 7.0      
}

education_mapping = {
    "Never Attended School": 1.0,
    "Elementary School": 2.0,
    "High School": 3.0,
    "High School Graduate": 4.0,
    "Some College": 5.0,
    "College Graduate": 6.0
}

genhlth_mapping = {
    "Excellent": 1.0,
    "Very Good": 2.0,
    "Good": 3.0,
    "Fair": 4.0,
    "Poor": 5.0
}

smoke_mapping = {
    "Never Smoked": 4.0,
    "Former Smoker": 3.0,
    "Smoke Some days": 2.0,
    "Smoke Everyday": 1.0
}

checkup_mapping = {
    "Never": 0.0,        
    "Within the past year": 1.0,
    "Within the past 2 years": 2.0,
    "Within the past 5 years": 3.0,
    "5 or more years ago": 4.0
}

feature_name_mapping = {
    '_RFBING5' : "General health not good (Fair/Poor)",
    '_RFHLTH': "Health risk",
    '_HCVU651': "Has healthcare insurance",
    '_TOTINDA': "Total physical Activity",
    'QLACTLM2': "Physical activities affected by health",
    '_AIDTST3': "Tested for HIV/AIDS",
    'HIVTST6' : "Tested for HIV/AIDS",    
    '_ASTHMS1': "Current asthma Status",
    'CHCSCNCR' : "Ever diagnosed with non-skin cancer",
    'CHCOCNCR': "Ever diagnosed with skin cancer",
    'ADDEPEV2': "Ever diagnosed with depressive disorder",
    '_DRDXAR1': "Diagnosed with arthritis by a doctor",
    'HAVARTH3': "Diagnosed with arthritis",
    'CHCKIDNY': "Ever Diagnosed with kidney disease",
    'CVDSTRK3': "Ever diagnosed with stroke",
    'CVDCRHD4': "Ever diagnosed with a coronary heart disease",
    'CVDINFR4': "Ever had a heart attack",
    'CHECKUP1': "Time since last routine medical checkup",
    'PERSDOC2': "Has a personal doctor",
    'MEDCOST': "Could not afford a doctor due to cost",
    'HLTHPLN1': "Has Healthcare Insurance",
    '_CHLDCNT': "Number of children in household",
    '_SMOKER3': "Smoking status",
    'ALCDAY5': "Alcohol consumption frequency",
    'DRNKANY5': "Consumed alcohol in the past 30 days",
    'EXERANY2': "Exercise during past month",
    'MENTHLTH': "Number of days mental health was bad in the last 30 days",
    'PHYSHLTH': "Number of days physical health was bad in the last 30 days",
    'GENHLTH': "General health status",
    'EDUCA': "Education level",
    'INCOME2': "Household income category",
    '_BMI5': "Body mass index (calculated using height and weight)",
    '_AGEG5YR': "Age category",
    'SEX': "Your sex"
}

if st.session_state['page'] == 'form':
    st.title("Diabetes Risk Predictor")
    st.caption(
    "This tool is for screening only. It flags people for further testing and does not provide a diagnosis."
    )

    with st.form("risk_inputs"):
        st.subheader("About You")
        st.caption("Basic demographics help estimate baseline risk.")
        col1, col2, col3, col4,ccol = st.columns(5)       
        
        with col1:
            age = st.slider("How old are you?", 18, 100, 25)
            age = map_to_age_band(age)

        with col2:
            sex_option = st.selectbox(
                "What is your biological sex?",
                ("Male", "Female", "Prefer not to say")
            )
            sex_encoded = 1 if sex_option=="Male" else 0
        
        with ccol:
            children = st.slider("How many children do you have?",0,5,0)
            st.caption("Select 0 or none if not applicable")

        with col3:
            income = st.selectbox(
                "Annual Household Income",
                (
                    "Less than $15,000",
                    "$15,000 - $25,000",
                    "$25,000 - $50,000",
                    "$50,000 - $75,000",
                    "$75,000 or more"
                )
            )
            income = income_mapping[income]
        with col4:
            education = st.selectbox(
                "Education Level",
                (
                    "Never Attended School",
                    "Elementary School",
                    "High School",
                    "High School Graduate",
                    "Some College",
                    "College Graduate"
                )
            )
            education = education_mapping[education]

        st.subheader("Your Body")
        st.caption("Height and weight are used to calculate BMI.")
        col5, col6 = st.columns(2)
        with col5:
            height = st.number_input(
                "Enter your height in cm",
                min_value=50.0,
                max_value=250.0,
                value=170.0,
                step=0.5
            )
            height_in_m = height / 100
        with col6:
            weight = st.number_input(
                "Enter your weight in kg",
                min_value=20.0,
                max_value=300.0,
                value=70.0,
                step=0.5
            )

        if height_in_m > 0:
            bmi = weight / (height_in_m ** 2)
            st.caption(f"Calculated BMI: {bmi:.1f}")
            st.caption("BMI is a screening indicator and does not replace clinical assessment.")

        st.subheader("Lifestyle")
        col7,col8,col9 = st.columns(3)
        with col7: 
            exerany2 = st.radio("Did you exercise in the past 30 days?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col8:
            smoking = st.selectbox(
                "What is your current smoking status?",
                ("Never Smoked","Former Smoker","Smoke Some days","Smoke Everyday")
            )
            smoking = smoke_mapping[smoking]
            qlactlm2 = st.radio("Are you limited in activities due to health?",
                                options=[1,0],
                                format_func=lambda x: "Yes" if x == 1 else "No")
        with col9:
            alcohol_days = st.slider("How many days did you drink in past 30 days?", 0, 30, 0)
            st.caption("Select 0 if you don't drink")

        st.subheader("Recent Health")
        col10,col11,col12 = st.columns(3)
        with col10:
            general_health = st.selectbox(
                "How would you rate your general health?",
                ("Excellent","Very Good","Good","Fair","Poor")
            )
            general_health = genhlth_mapping[general_health]
        with col11:
            physical_health = st.slider("In the past 30 days, how many days was your physical health not good?",0,30,0)
        with col12:
            mental_health = st.slider("In the past 30 days, how many days was your mental health not good?",0,30,0)

        st.subheader("Medical History")
        col13,col14,col15,col16,col17,col18,col19,col20 = st.columns(8)
        with col13:
            heart_attack = st.radio("Have you ever had a heart attack?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

            coronary_disease = st.radio("Have you ever had coronary heart disease?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

        with col14:
            stroke = st.radio("Have you ever had a stroke?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

        with col15:
            arthritis = st.radio("Have you ever had arthritis?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

            dr_arthritis = st.radio("Have you ever been diagnosed with arthritis by a doctor?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col16:
            kidney_disease = st.radio("Have you ever had kidney disease?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

        with col17:
            depression = st.radio("Have you ever had depression?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

        with col18:
            skin_cancer = st.radio("Have you ever had skin cancer?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

            other_cancer = st.radio("Have you ever had any other cancer?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col19:
            asthma = st.selectbox(
                "What is your current asthma status?",
                ("Never","Former","Current")
            )
            asthma = asthma_mapping[asthma]

        with col20:
            hiv = st.radio("Have you ever been tested for HIV?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")

        st.subheader("Healthcare Access")
        col21,col22,col23,col24 = st.columns(4)
        with col21:
            hlthplan = st.radio("Do you have health insurance?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col22:
            medcost = st.radio("In the past year, did you avoid the doctor due to cost?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col23:
            persdoc = st.radio("Do you have a personal doctor?", 
                        options=[1, 0],
                        format_func=lambda x: "Yes" if x == 1 else "No")
        with col24:
            checkup = st.selectbox(
                "When was your last routine checkup?",
                ("Within the past year","Within the past 2 years","Within the past 5 years","5 or more years ago","Never")
            )
            checkup = checkup_mapping[checkup]

        submitted = st.form_submit_button("Run Risk Screening")
    
    
    
    totinda = exerany2
    rfhlth = 1 if general_health>=3.0 else 0
    hcvu651 = hlthplan
    rfbing5 = 1 if alcohol_days>=5 else 0
    aidtst3 = hiv
    drnkany5 = 1 if alcohol_days>1 else 0

    if submitted:
        input_dict = {
                '_RFBING5' : rfbing5,
                '_RFHLTH': rfhlth,
                '_HCVU651': hlthplan,
                '_TOTINDA': totinda,
                'QLACTLM2': qlactlm2,
                '_AIDTST3':aidtst3,
                'HIVTST6' : hiv,
                '_ASTHMS1': asthma,
                'CHCSCNCR' : other_cancer,
                'CHCOCNCR':skin_cancer,
                'ADDEPEV2':depression,
                '_DRDXAR1':dr_arthritis,
                'HAVARTH3':arthritis,
                'CHCKIDNY':kidney_disease,
                'CVDSTRK3':stroke,
                'CVDCRHD4':coronary_disease,
                'CVDINFR4':heart_attack,
                'CHECKUP1':checkup,
                'PERSDOC2':persdoc,
                'MEDCOST':medcost,
                'HLTHPLN1':hlthplan,
                '_CHLDCNT': float(children + 1),  # shift 0-5 → 1-6
                '_SMOKER3':smoking,
                'ALCDAY5':alcohol_days,
                'DRNKANY5':drnkany5,
                'EXERANY2':exerany2,
                'MENTHLTH':mental_health,
                'PHYSHLTH':physical_health,
                'GENHLTH':general_health,
                'EDUCA':education,
                'INCOME2':income,
                '_BMI5':bmi,
                '_AGEG5YR':age,
                'SEX':sex_encoded
        }
        input_df = pd.DataFrame([input_dict])
        binary_cols = ["_RFBING5",'_AIDTST3','HLTHPLN1','QLACTLM2','CHCOCNCR','_RFHLTH','HAVARTH3','HIVTST6','MEDCOST','CHCSCNCR','EXERANY2','DRNKANY5','_HCVU651','ADDEPEV2','PERSDOC2','CVDSTRK3','_TOTINDA','CHCKIDNY','CVDCRHD4','CVDINFR4','SEX','_DRDXAR1']
        continous_cols = ["PHYSHLTH",'_BMI5','ALCDAY5','MENTHLTH']
        ordinal_cols = ["_SMOKER3","GENHLTH",'_AGEG5YR','INCOME2','EDUCA','_ASTHMS1',"CHECKUP1",'_CHLDCNT']

        all_cols = binary_cols + continous_cols + ordinal_cols
        input_df = input_df[all_cols]
        input_df = input_df.astype(float)
        input_scaled = preprocessor.transform(input_df)
        proba = model.predict_proba(input_scaled)[0][1]

        if proba<0.40:
                risk_category = "Low Risk"
                risk_emoji = "✅"
        elif proba < 0.73:
                risk_category = "Medium Risk"
                risk_emoji = "⚠️"
        else: 
                risk_category = "High Risk"
                risk_color = "red"
                risk_emoji = "🔴"

        #SHAP Calculation
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_scaled)

        #Top 3 contributing features
        feature_names = all_cols
        shap_df = pd.DataFrame({
                    'feature' : feature_names,
                    'shap_value': shap_values[0]
        }).sort_values("shap_value",key=abs,ascending=False)

        increasers = shap_df[shap_df['shap_value']>0].head(3)
        decreasers = shap_df[shap_df['shap_value']<0].head(2)

        st.session_state['proba'] = proba
        st.session_state['risk_category'] = risk_category
        st.session_state['risk_emoji'] = risk_emoji
        st.session_state['increasers'] = increasers
        st.session_state['decreasers'] = decreasers
        st.session_state['input_df'] = input_df
        st.session_state['page'] = 'results'
        st.rerun()



elif st.session_state['page'] == 'results':
    proba = st.session_state['proba']
    risk_category = st.session_state['risk_category']
    risk_emoji = st.session_state['risk_emoji']
    increasers = st.session_state['increasers']
    decreasers = st.session_state['decreasers']
    input_df = st.session_state['input_df']
    
    st.subheader("Your Results")

    res_col1,res_col2 = st.columns(2)

    with res_col1:
            st.markdown(f"### {risk_emoji} {risk_category}")
            st.markdown(f"**Risk Score: {proba*100:.1f}%**")
            st.markdown("Score reflects model confidence, not certainty of diagnosis")

            st.markdown("#### Why this score?")

            value_display = {
                 '_SMOKER3': {4.0: "Never Smoked",3.0: "Former Smoker",2.0: "Smoke Some days",1.0: "Smoke Everyday"},
                 'GENHLTH' : {1.0: "Excellent",2.0: "Very Good",3.0: "Good",4.0: "Fair",5.0: "Poor"},
                 'SEX': {1.0: 'Male', 0.0: 'Female'},
                 '_ASTHMS1': {1.0: "Never",2.0: "Former",3.0: "Current"},
                 'INCOME2': {1.0: "Less than $15,000",2.0: "$15,000 - $25,000",4.0: "$25,000 - $50,000",6.0: "$50,000 - $75,000",7.0: "$75,000 or more"},
                 'EDUCA': {1.0: "Never Attended School",2.0: "Elementary School",3.0: "High School",4.0: "High School Graduate",5.0: "Some College",6.0: "College Graduate"},
                 'CHECKUP1': {0.0: "Never",1.0: "Within the past year",2.0: "Within the past 2 years",3.0: "Within the past 5 years",4.0: "5 or more years ago"},
                 '_AGEG5YR': {
                    1.0: '18-24', 2.0: '25-29', 3.0: '30-34', 4.0: '35-39',
                    5.0: '40-44', 6.0: '45-49', 7.0: '50-54', 8.0: '55-59',
                    9.0: '60-64', 10.0: '65-69', 11.0: '70-74', 12.0: '75-79',
                    13.0: '80-84', 14.0: '85+'
                    }
            }

            st.markdown("**Factors increasing your risk:**")
            for _, row in increasers.iterrows():
                readable = feature_name_mapping.get(row['feature'], row['feature'])
                raw_val = input_df[row['feature']].values[0]
                val_label = value_display.get(row["feature"],{}).get(raw_val,"")
                display = f"**{readable}**" + (f"({val_label})" if val_label else "")
                st.markdown(f"🔴 {display}")

                
            st.markdown("**Factors reducing your risk:**")
            for _, row in decreasers.iterrows():
                readable = feature_name_mapping.get(row['feature'], row['feature'])
                raw_val = input_df[row['feature']].values[0]
                val_label = value_display.get(row["feature"],{}).get(raw_val,"")
                display = f"**{readable}**" + (f"({val_label})" if val_label else "")
                st.markdown(f"🟢 {display}")

            st.caption("""
            ⚠️ SHAP explanations show statistical associations learned from 
            survey data — not clinical causation. Some factors may appear 
            counterintuitive due to reverse causality in self-reported data.
            Always consult a healthcare provider for clinical interpretation.
            """)

    with res_col2:
            if risk_category == "Low Risk":
                st.success("Your responses suggest low diabetes risk. Maintain your healthy lifestyle")
            elif risk_category == "Medium Risk":
                st.warning("Your responses suggest moderate risk factors. Consider speaking with a doctor.")
            else:
                st.error("Your responses suggest several risk factors. Please consult a healthcare provider.")

    st.markdown("#### Recommended Next Steps")
    if risk_category == "Low Risk":
            st.markdown("""
            - ✅ Maintain your current healthy lifestyle
            - 📅 Schedule annual routine checkup
            - 🥗 Continue balanced diet and regular exercise
            """)
    elif risk_category == "Medium Risk":
            st.markdown("""
            - 🩺 Schedule a checkup with your doctor
            - 🩸 Request a fasting blood glucose test
            - 🏃 Increase physical activity if possible
            - 🥗 Review dietary habits
            """)
    else:
            st.markdown("""
            - 🚨 Consult a healthcare provider soon
            - 🩸 Request HbA1c and fasting glucose tests immediately
            - 📋 Discuss family history with your doctor
            - 🏃 Begin supervised exercise program
            - 🥗 Consult a nutritionist
            """)

    if st.button("← Back to Screening"):
         st.session_state['page'] = 'form'
         st.rerun()