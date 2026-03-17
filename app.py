import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Space Uber", page_icon="🚀", layout="centered")

# Constants
MU = 398600
EARTH_RADIUS = 6371

# Functions
def hohmann_delta_v(h1, h2):
    r1 = EARTH_RADIUS + h1
    r2 = EARTH_RADIUS + h2

    v1 = math.sqrt(MU / r1)
    v_transfer1 = math.sqrt(MU * (2*r2 / (r1 + r2)) / r1)
    dv1 = v_transfer1 - v1

    v2 = math.sqrt(MU / r2)
    v_transfer2 = math.sqrt(MU * (2*r1 / (r1 + r2)) / r2)
    dv2 = v2 - v_transfer2

    return abs(dv1) + abs(dv2)

def calculate_price(dv, urgency):
    base_fee = 1000
    fuel_cost = 500
    return base_fee + dv * fuel_cost * urgency

# UI Title
st.markdown(
    """
    <h1 style='text-align: center; color: cyan;'>🚀 Space Uber</h1>
    <h3 style='text-align: center;'>Orbital Transfer Cost Calculator</h3>
    <hr>
    """,
    unsafe_allow_html=True
)

# Satellite Selection
st.subheader("🛰 Mission Inputs")

selected_sat = st.selectbox("Choose Satellite", [
    "Custom",
    "ISS (420 km)",
    "Starlink (550 km)",
    "GPS (20200 km)"
])

# Altitude Logic
if selected_sat == "ISS (420 km)":
    alt1 = 420
    st.info("Using ISS orbit (420 km)")

elif selected_sat == "Starlink (550 km)":
    alt1 = 550
    st.info("Using Starlink orbit (550 km)")

elif selected_sat == "GPS (20200 km)":
    alt1 = 20200
    st.info("Using GPS orbit (20200 km)")

else:
    alt1 = st.slider("Current Orbit (km)", 200, 2000, 400)

alt2 = st.slider("Target Orbit (km)", 200, 36000, 800)
urgency = st.slider("Urgency Multiplier", 1.0, 3.0, 1.0)

# Button
if st.button("🚀 Calculate Transfer"):

    dv = hohmann_delta_v(alt1, alt2)
    price = calculate_price(dv, urgency)

    # Results
    st.subheader("📊 Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Δv (km/s)", f"{dv:.2f}")

    with col2:
        st.metric("Cost ($)", f"{price:.2f}")

    # AI Suggestion
    st.subheader("🤖 Smart Suggestion")

    if dv < 1:
        st.success("Efficient transfer. Proceed!")
    elif dv < 2:
        st.info("Consider optimizing orbit slightly.")
    elif dv < 3:
        st.warning("Moderate cost transfer.")
    else:
        st.error("Avoid this transfer. Too expensive!")

    # Collision Risk
    st.subheader("🚨 Collision Risk Analysis")

    if abs(alt2 - alt1) > 1000:
        st.error("High Risk: Possible debris field crossing!")
    elif abs(alt2 - alt1) > 500:
        st.warning("Medium Risk: Debris zone possible.")
    else:
        st.success("Low Risk Transfer.")

    if alt2 > 20000:
        st.warning("High-altitude congestion zone.")

    # Visualization
    st.subheader("🛰 Orbit Visualization")

    theta = np.linspace(0, 2*np.pi, 100)

    r1 = EARTH_RADIUS + alt1
    r2 = EARTH_RADIUS + alt2

    x1 = r1 * np.cos(theta)
    y1 = r1 * np.sin(theta)

    x2 = r2 * np.cos(theta)
    y2 = r2 * np.sin(theta)

    fig, ax = plt.subplots()

    earth = plt.Circle((0, 0), EARTH_RADIUS, fill=False)
    ax.add_artist(earth)

    ax.plot(x1, y1, label="Current Orbit")
    ax.plot(x2, y2, label="Target Orbit")

    ax.set_aspect('equal')
    ax.legend()

    st.pyplot(fig)