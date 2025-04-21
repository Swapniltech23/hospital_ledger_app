import streamlit as st
import hashlib

# Generate a SHA-256 hash for the visit
def generate_hash(patient_name, treatment, cost, date_of_visit):
    visit_data = patient_name + treatment + str(cost) + date_of_visit
    return hashlib.sha256(visit_data.encode()).hexdigest()

# Initialize ledger using session state
if "hospital_ledger" not in st.session_state:
    st.session_state.hospital_ledger = {}

st.title("🏥 Hospital Visit Ledger")

# --- Form to Add Visit ---
st.header("Add a Patient Visit")

with st.form("visit_form"):
    patient_name = st.text_input("Patient Name")
    treatment = st.text_input("Treatment Received")
    cost = st.number_input("Cost ($)", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Date of Visit")

    submitted = st.form_submit_button("Add Visit")

    if submitted:
        visit_hash = generate_hash(patient_name, treatment, cost, str(date_of_visit))

        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": str(date_of_visit),
            "visit_hash": visit_hash
        }

        if patient_name not in st.session_state.hospital_ledger:
            st.session_state.hospital_ledger[patient_name] = []

        st.session_state.hospital_ledger[patient_name].append(visit)
        st.success(f"Visit added for {patient_name} on {date_of_visit} (Treatment: {treatment}, Cost: ${cost})")
        st.code(visit_hash, language='text')

# --- Section to View Patient Visits ---
st.header("🔍 Search Patient Records")

if st.session_state.hospital_ledger:
    selected_patient = st.selectbox("Select Patient", list(st.session_state.hospital_ledger.keys()))

    if selected_patient:
        st.subheader(f"Visit Records for {selected_patient}")
        for i, visit in enumerate(st.session_state.hospital_ledger[selected_patient], 1):
            with st.expander(f"Visit {i} - {visit['date_of_visit']}"):
                st.write(f"**Treatment:** {visit['treatment']}")
                st.write(f"**Cost:** ${visit['cost']}")
                st.write(f"**Hash:** `{visit['visit_hash']}`")
else:
    st.info("No patient records available. Add a visit to get started.")
