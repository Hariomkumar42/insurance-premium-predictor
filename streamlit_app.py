
import streamlit as st
import requests

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="InsureAI | Premium Predictor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/predict"
API_HEALTH_URL = "http://127.0.0.1:8000/docs"

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #152d4a 0%, transparent 35%),
        #080d19;
    color: #f1f5ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #0d1525;
    border-right: 1px solid #24334b;
}

section[data-testid="stSidebar"] label {
    color: #d8e2f2;
}

.hero {
    padding: 27px 30px;
    border: 1px solid #293b53;
    border-radius: 22px;
    background: linear-gradient(115deg, #14243a, #102522);
    margin-bottom: 25px;
}

.eyebrow {
    color: #5ce1c1;
    font-size: 11px;
    letter-spacing: 2.2px;
    font-weight: 800;
}

.hero-title {
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -1.5px;
    margin: 13px 0;
    color: #f5f8ff;
}

.hero-title span {
    color: #5ce1c1;
}

.hero-subtitle {
    color: #a5b4cb;
    line-height: 1.8;
    font-size: 14px;
    max-width: 780px;
}

.panel {
    background: rgba(17, 26, 43, .94);
    border: 1px solid #27364e;
    border-radius: 19px;
    padding: 22px;
    margin-bottom: 18px;
}

.panel-title {
    font-size: 18px;
    font-weight: 750;
    color: #f3f7ff;
    margin-bottom: 5px;
}

.panel-subtitle {
    font-size: 12px;
    color: #96a7c0;
    margin-bottom: 20px;
}

.insight {
    background: #0b1423;
    border: 1px solid #283750;
    border-radius: 13px;
    padding: 16px;
    margin-bottom: 12px;
}

.insight-label {
    color: #91a4c0;
    font-size: 11px;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.insight-value {
    color: #5ce1c1;
    font-size: 24px;
    font-weight: 800;
}

.insight-note {
    color: #9aabc2;
    font-size: 11px;
    margin-top: 6px;
}

.result-panel {
    background: linear-gradient(145deg, #15352f, #101b2b 75%);
    border: 1px solid #326257;
    border-radius: 19px;
    padding: 25px;
    margin-top: 15px;
}

.result-label {
    color: #5ce1c1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.result-value {
    color: #f5fffc;
    font-size: clamp(25px, 3vw, 38px);
    font-weight: 800;
    margin: 13px 0;
    overflow-wrap: anywhere;
}

.small-muted {
    color: #a1b2c9;
    font-size: 12px;
    line-height: 1.7;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(100deg, #5ce1c1, #a4f0d8);
    color: #071b1b;
    border: none;
    border-radius: 11px;
    font-weight: 800;
    min-height: 47px;
    transition: all .2s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    color: #071b1b;
    border: none;
    filter: brightness(1.08);
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    background: #111a2b;
    border: 1px solid #293850;
    border-radius: 14px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #a6b6cd;
}

div[data-testid="stMetricValue"] {
    color: #5ce1c1;
}

hr {
    border-color: #26364d;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ---------------- CITY CLASSIFICATION ----------------

TIER_1_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

TIER_2_CITIES = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna",
    "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal",
    "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur",
    "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun",
    "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram",
    "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad",
    "Hubli", "Belgaum", "Salem", "Vijayawada",
    "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad",
    "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur",
    "Asansol", "Siliguri"
]


def get_city_tier(city):
    city = city.strip().casefold()

    if city in [c.casefold() for c in TIER_1_CITIES]:
        return 1
    elif city in [c.casefold() for c in TIER_2_CITIES]:
        return 2
    return 3


def get_age_group(age):
    if age < 25:
        return "Young"
    elif age < 45:
        return "Adult"
    elif age < 60:
        return "Middle-aged"
    return "Senior"


def get_lifestyle_risk(bmi, smoker):
    if smoker and bmi > 30:
        return "High"
    elif smoker or bmi > 27:
        return "Medium"
    return "Low"


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ✦ InsureAI")
    st.caption("INTELLIGENT PREMIUM ANALYTICS")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("🏠  Premium Predictor")
    st.markdown("🧠  Model Insights")
    st.markdown("⚙️  API Connection")

    st.divider()

    st.markdown("### About this project")
    st.write(
        "An interactive frontend connected to a trained "
        "machine learning model through FastAPI."
    )

    st.markdown("### Technology stack")
    st.markdown(
        "- Python\n"
        "- Streamlit\n"
        "- FastAPI\n"
        "- Scikit-learn\n"
        "- Pandas"
    )

    st.divider()

    if st.button("🔌 Check API connection", use_container_width=True):
        try:
            response = requests.get(API_HEALTH_URL, timeout=3)
            if response.ok:
                st.success("FastAPI is reachable!")
            else:
                st.warning(f"API returned status {response.status_code}")
        except requests.RequestException:
            st.error("Cannot reach FastAPI. Start your backend first.")


# ---------------- HERO HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-POWERED PREDICTION PLATFORM</div>
    <div class="hero-title">
        Understand your risk.<br>
        <span>Predict smarter.</span>
    </div>
    <div class="hero-subtitle">
        Explore how personal details, lifestyle and city classification
        are processed by your machine learning model to predict an
        insurance premium category.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- PROFILE INPUTS ----------------

st.markdown("### ◈ Your profile")
st.markdown(
    '<p class="small-muted">Enter your details to generate a model prediction.</p>',
    unsafe_allow_html=True
)

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="panel-title">Personal information</div>'
        '<div class="panel-subtitle">Your details and lifestyle preferences</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age (years)",
            min_value=1,
            max_value=119,
            value=28,
            step=1
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=70.0,
            step=0.5
        )

        income = st.number_input(
            "Annual income (LPA)",
            min_value=0.1,
            max_value=10000.0,
            value=8.0,
            step=0.5
        )

    with col2:
        height = st.number_input(
            "Height (metres)",
            min_value=0.1,
            max_value=2.49,
            value=1.72,
            step=0.01,
            format="%.2f"
        )

        city = st.text_input(
            "City",
            value="Patna",
            help="Enter a city name. Unlisted cities are classified as Tier 3."
        )

        occupation = st.selectbox(
            "Occupation",
            [
                "student",
                "private_job",
                "government_job",
                "business_owner",
                "freelancer",
                "unemployed",
                "retired"
            ],
            format_func=lambda x: x.replace("_", " ").title()
        )

    smoker = st.toggle("🚬  Do you smoke?", value=False)

    st.markdown("<br>", unsafe_allow_html=True)

    predict_button = st.button(
        "✦  Predict Premium Category",
        use_container_width=True,
        type="primary"
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- LIVE PROFILE INSIGHTS ----------------

bmi = weight / (height ** 2)
age_group = get_age_group(age)
city_tier = get_city_tier(city)
lifestyle_risk = get_lifestyle_risk(bmi, smoker)

with right:
    st.markdown(
        '<div class="panel-title">✧ Live profile insights</div>'
        '<div class="panel-subtitle">Updates as you change your details</div>',
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(2)

    with m1:
        st.markdown(
            f"""
            <div class="insight">
                <div class="insight-label">BODY MASS INDEX</div>
                <div class="insight-value">{bmi:.2f}</div>
                <div class="insight-note">Weight / height²</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div class="insight">
                <div class="insight-label">CITY CLASSIFICATION</div>
                <div class="insight-value">Tier {city_tier}</div>
                <div class="insight-note">Based on city list</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">AGE GROUP</div>
            <div class="insight-value">{age_group}</div>
            <div class="insight-note">Derived from your age</div>
        </div>
        <div class="insight">
            <div class="insight-label">LIFESTYLE INDICATOR</div>
            <div class="insight-value">{lifestyle_risk}</div>
            <div class="insight-note">
                Rule-based indicator using smoking status and BMI.
                This is not a medical assessment.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-muted">
            These insights are calculated in the frontend for immediate
            feedback. The actual category prediction comes from your
            trained model through the FastAPI backend.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- MODEL PREDICTION ----------------

if predict_button:
    if not city.strip():
        st.error("Please enter a city name.")
    else:
        payload = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income),
            "smoker": bool(smoker),
            "city": city.strip(),
            "occupation": occupation
        }

        with st.spinner("Connecting to the model and analyzing your profile..."):
            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )

                if response.ok:
                    result = response.json()

                    if "predicted_category" not in result:
                        st.error(
                            "The API response did not contain "
                            "'predicted_category'. Check your FastAPI code."
                        )
                    else:
                        st.session_state["prediction_result"] = result
                        st.session_state["prediction_payload"] = payload

                else:
                    try:
                        details = response.json()
                    except ValueError:
                        details = response.text

                    st.error(
                        f"Prediction failed (HTTP {response.status_code}). "
                        f"Details: {details}"
                    )

            except requests.RequestException as error:
                st.error(
                    "Could not connect to FastAPI. Make sure your backend "
                    "is running at http://127.0.0.1:8000.\n\n"
                    f"Technical details: {error}"
                )


# ---------------- DISPLAY RESULT ----------------

st.divider()

st.markdown("### ✨ Prediction result")

if "prediction_result" in st.session_state:
    result = st.session_state["prediction_result"]
    category = result["predicted_category"]

    st.markdown(
        f"""
        <div class="result-panel">
            <div class="result-label">MODEL OUTPUT</div>
            <div class="result-value">{category}</div>
            <div class="small-muted">
                Your trained machine learning model returned this
                predicted premium category successfully.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("Prediction completed successfully.")

    with st.expander("View submitted data and raw API response"):
        st.markdown("**Input sent to FastAPI**")
        st.json(st.session_state["prediction_payload"])

        st.markdown("**Response received from model**")
        st.json(result)

else:
    st.markdown(
        """
        <div class="result-panel">
            <div class="result-label">READY FOR ANALYSIS</div>
            <div class="result-value">Your prediction awaits</div>
            <div class="small-muted">
                Complete the profile on the left and select
                Predict Premium Category. Your model's output
                will appear here.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- FOOTER ----------------

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#8192aa; font-size:11px;">
        INSUREAI · MACHINE LEARNING PROJECT · POWERED BY STREAMLIT + FASTAPI
        <br><br>
        Educational demonstration only. This prediction is not an
        official insurance quote or a medical assessment.
    </div>
    """,
    unsafe_allow_html=True
)
