import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Corporate Training Platform", layout="wide")

# --- SESSION STATE (ADDED) ---
if "run" not in st.session_state:
    st.session_state.run = False

# --- CUSTOM CSS (clean cards) ---
st.markdown("""
<style>
.card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 8px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚙️ Controls")

total_employees = st.sidebar.slider("Employees", 50, 500, 200)
growth_rate = st.sidebar.slider("Growth Rate", 0.1, 1.0, 0.3)
network_effect = st.sidebar.slider("Network Effect", 0.0, 1.0, 0.2)
dropout_rate = st.sidebar.slider("Dropout Rate", 0.0, 0.5, 0.05)
time_steps = st.sidebar.slider("Time Steps", 10, 100, 40)

# --- BUTTONS (ADDED) ---
if st.sidebar.button("🚀 Run Simulation"):
    st.session_state.run = True

if st.sidebar.button("🔄 Reset"):
    st.session_state.run = False
    st.rerun()

# --- HEADER ---
st.title("🏢 Corporate Training Platform Adoption Dashboard")
st.caption("Logistic Growth + Network Effects + Dropout Analysis")

# --- STOP INITIAL OUTPUT (ADDED) ---
if not st.session_state.run:
    st.info("👉 Set parameters and click 'Run Simulation'")
    st.stop()

# --- SIMULATION ---
def simulate():
    users = 1
    active = 1

    user_hist, active_hist, dropout_hist = [], [], []

    for t in range(time_steps):
        new_users = growth_rate * users * (1 - users / total_employees)
        network_boost = network_effect * users

        users = users + new_users + network_boost

        dropouts = dropout_rate * active
        active = users - dropouts

        user_hist.append(users)
        active_hist.append(active)
        dropout_hist.append(dropouts)

    return user_hist, active_hist, dropout_hist

users, active, dropouts = simulate()

# --- METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='card'>👥<h3>{total_employees}</h3><p>Total Employees</p></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'>📈<h3>{growth_rate}</h3><p>Growth Rate</p></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'>🌐<h3>{network_effect}</h3><p>Network Effect</p></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='card'>❌<h3>{dropout_rate}</h3><p>Dropout Rate</p></div>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
left, right = st.columns([2, 1])

# --- GRAPH (LEFT SIDE) ---
with left:
    st.subheader("📊 Adoption Trends")

    fig, ax = plt.subplots()
    ax.plot(users, label="Registered Users")
    ax.plot(active, label="Active Users")
    ax.plot(dropouts, label="Dropouts")

    ax.set_xlabel("Time")
    ax.set_ylabel("Users")
    ax.legend()

    st.pyplot(fig)

# --- ANALYSIS (RIGHT SIDE) ---
with right:
    st.subheader("📉 Analysis")

    peak = int(max(active))
    final_users = int(users[-1])

    st.metric("🔥 Peak Active Users", peak)
    st.metric("📊 Final Users", final_users)

    # --- Insights ---
    st.subheader("💡 Insights")

    if network_effect > 0.5:
        st.success("🚀 Strong network effect → rapid adoption")
    else:
        st.warning("⚠️ Weak network effect → slow growth")

    if dropout_rate > 0.2:
        st.error("❌ High dropout → retention issue")
    else:
        st.success("✅ Good retention")

    st.info("📌 Improve engagement to boost adoption")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed using Streamlit | Mathematical Modeling Project")
