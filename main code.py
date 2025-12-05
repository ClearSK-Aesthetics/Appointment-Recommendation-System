import streamlit as st
import math
import requests

# Google Maps API Key (stored inside Streamlit Secrets)
API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]

# Fixed Clinic List
clinics = [
    {"name": "ClearSK Premier Aesthetic Clinic(Scotts)", "code": "SMC", "postal": "228210"},
    {"name": "ClearSK Aesthetic Clinic(Novena)", "code": "NMC", "postal": "307506"},
    {"name": "ClearSK Aesthetic Clinic(Kovan)", "code": "KV", "postal": "530205"},
    {"name": "ClearSK Aesthetic Clinic(Westgate)", "code": "WG", "postal": "608532"},
    {"name": "ClearSK Aesthetic Clinic(Raffles Place)", "code": "RP", "postal": "048616"},
]

# Utility Functions
def validate_postal(p):
    """Ensure postal code is a valid 6-digit Singapore postal."""
    if not p:
        return None
    p = p.strip().replace(" ", "")
    return p if len(p) == 6 and p.isdigit() else None


@st.cache_data
def geocode(postal):
    """Convert postal code into latitude & longitude using Google Maps API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": postal, "region": "sg", "key": API_KEY}
    response = requests.get(url, params=params).json()

    if response["status"] != "OK":
        raise ValueError(f"Postal code {postal} could not be located.")

    location = response["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


def haversine(lat1, lon1, lat2, lon2):
    """Compute distance between two lat/lon pairs using the Haversine formula."""
    R = 6371  # Earth radius in km
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# Streamlit UI

st.set_page_config(page_title="Clinic Appointment Recommender", layout="wide")
col1,col2=st.column([1,5])

with col1:
    st.image("Appointment Advisor.png",width=180)
with col2:
    st.markdown("""
<style>
.header-container {
    display: flex;
    align-items: center;
    gap: 20px;
}
</style>

<div class="header-container">
    <img src="branding.png" width="180">
    <h2>Clinic Appointment Recommender</h2>
</div>
""", unsafe_allow_html=True)
st.title("Clinic Appointment Recommender")
st.write("Find the nearest clinics based on your home and work locations.")

# ----------------- User Inputs -----------------

home_raw = st.text_input("Home Postal Code (6 digits)", placeholder="e.g. 307506")
work_raw = st.text_input("Work Postal Code (6 digits)", placeholder="e.g. 238859")

home_postal = validate_postal(home_raw)
work_postal = validate_postal(work_raw)

if home_raw and not home_postal:
    st.error("❌ Invalid home postal code. Please enter a 6-digit code.")

if work_raw and not work_postal:
    st.error("❌ Invalid work postal code. Please enter a 6-digit code.")

preferred_days = st.multiselect(
    "Select any 2 preferred days",
    ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    max_selections=2
)

col1, col2 = st.columns(2)
with col1:
    am = st.checkbox("AM Slot (11am – 2pm)")
with col2:
    pm = st.radio("PM Slot:", ["None", "4pm – 6pm", "7pm – 9pm"], index=0)

# ----------------- Compute Button -----------------

if st.button("Recommend Clinics"):
    if not home_postal or not work_postal:
        st.error("⚠️ Please enter valid postal codes for both Home and Work.")
    else:
        try:
            # Geocode inputs
            home_lat, home_lng = geocode(home_postal)
            work_lat, work_lng = geocode(work_postal)

            # Compute distance to each clinic
            for c in clinics:
                clinic_lat, clinic_lng = geocode(c["postal"])
                c["dist_home"] = haversine(home_lat, home_lng, clinic_lat, clinic_lng)
                c["dist_work"] = haversine(work_lat, work_lng, clinic_lat, clinic_lng)

            nearest_home = min(clinics, key=lambda x: x["dist_home"])
            nearest_work = min(clinics, key=lambda x: x["dist_work"])

            # ---- Output: Nearest to Home ----
            st.subheader("Nearest Clinic to Home")
            st.info(f"""
**Clinic Name:** {nearest_home['name']} ({nearest_home['code']})  
**Postal Code:** {nearest_home['postal']}  
**Distance:** {nearest_home['dist_home']:.2f} km
            """)

            # ---- Output: Nearest to Work ----
            st.subheader("Nearest Clinic to Work")
            st.info(f"""
**Clinic Name:** {nearest_work['name']} ({nearest_work['code']})  
**Postal Code:** {nearest_work['postal']}  
**Distance:** {nearest_work['dist_work']:.2f} km
            """)

            # Show preferences (optional)
            st.markdown("---")
            st.write("### 📋 Your preferences (record only)")
            st.write("**Days selected:**", ", ".join(preferred_days) if preferred_days else "None")

            segments = []
            if am:
                segments.append("AM (11am–2pm)")
            if pm != "None":
                segments.append(pm)

            st.write("**Preferred time segments:**", ", ".join(segments) if segments else "None")

        except Exception as e:
            st.error(f"An error occurred: {e}")

