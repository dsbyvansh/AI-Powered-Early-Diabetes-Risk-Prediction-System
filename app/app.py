import streamlit as st
import joblib

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
    model = joblib.load('../models/xgboost_final.pkl')
    preprocessor = joblib.load('../models/preprocessor.pkl')
    return model,preprocessor

model,preprocessor = load_artifacts()

st.title("Diabetes Risk Predictor")
st.caption(
    "This tool is for screening only. It flags people for further testing and does not provide a diagnosis."
)


def map_to_age_band(age):
    if age < 25: return 0.0
    elif age < 30: return 1.0
    elif age < 35: return 2.0
    elif age < 40: return 3.0
    elif age < 45: return 4.0
    elif age < 50: return 5.0
    elif age < 55: return 6.0
    elif age < 60: return 7.0
    elif age < 65: return 8.0
    elif age < 70: return 9.0
    elif age < 75: return 10.0
    elif age < 80: return 11.0
    elif age < 85: return 12.0
    else: return 13.0 

asthma_mapping = {
    "Never": 0.0,      # BRFSS 1 → encoded 0
    "Former": 1.0,     # BRFSS 2 → encoded 1
    "Current": 2.0     # BRFSS 3 → encoded 2
}

income_mapping = {
    "Less than $15,000": 0.0,    # BRFSS 1 → encoded 0
    "$15,000 - $25,000": 2.0,    # BRFSS 3 → encoded 2
    "$25,000 - $50,000": 4.0,    # BRFSS 5 → encoded 4
    "$50,000 - $75,000": 6.0,    # BRFSS 7 → encoded 6
    "$75,000 or more": 7.0       # BRFSS 8 → encoded 7
}

education_mapping = {
    "Never Attended School": 0.0,
    "Elementary School": 1.0,
    "High School": 2.0,
    "High School Graduate": 3.0,
    "Some College": 4.0,
    "College Graduate": 5.0
}

genhlth_mapping = {
    "Excellent": 0.0,
    "Very Good": 1.0,
    "Good": 2.0,
    "Fair": 3.0,
    "Poor": 4.0
}

smoke_mapping = {
    "Never Smoked": 3.0,    # BRFSS 4 → encoded 3
    "Former Smoker": 2.0,   # BRFSS 3 → encoded 2
    "Smoke Some days": 1.0, # BRFSS 2 → encoded 1
    "Smoke Everyday": 0.0   # BRFSS 1 → encoded 0
}

checkup_mapping = {
    "Never": 0.0,
    "Within the past year": 1.0,
    "Within the past 2 years": 2.0,
    "Within the past 5 years": 3.0,
    "5 or more years ago": 4.0
}


with st.form("risk_inputs"):
    st.subheader("About You")
    st.caption("Basic demographics help estimate baseline risk.")
    col1, col2, col3, col4,ccol = st.columns(5)       
    
    with col1:
        age = st.slider("How old are you?", 18, 100, 25)
        age_band = map_to_age_band(age)
    with col2:
        sex_option = st.selectbox(
            "What is your biological sex?",
            ("Male", "Female", "Prefer not to say")
        )

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

    totinda = exerany2
    rfhlth = 1 if general_health in ["Fair","Poor"] else 0
    hcvu651 = hlthplan
    rfbing5 = 1 if alcohol_days>=5 else 0
    aidtst3 = hiv
    
    submitted = st.form_submit_button("Run Risk Screening")
    