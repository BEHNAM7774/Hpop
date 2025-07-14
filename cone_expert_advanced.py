
import streamlit as st
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.graph_objects as go

st.set_page_config(page_title="Cone Expert Pro", layout="centered", page_icon="🌀")

st.title("🌀 Cone Expert Pro")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🔺 Cone Calculator", "📐 Support Angle", "⚙️ Cutting Speed & Feed", "🧱 3D Cone View"])

# ========== Cone Calculator ==========
with tab1:
    D = st.number_input("Large Diameter D (mm)", value=50.0)
    d = st.number_input("Small Diameter d (mm)", value=30.0)
    l = st.number_input("Cone Length l (mm)", value=100.0)

    if st.button("🔍 Calculate Cone Angle"):
        if D > d and l > 0:
            delta = D - d
            tan_alpha_2 = delta / (2 * l)
            alpha_rad = math.atan(tan_alpha_2) * 2
            alpha_deg = math.degrees(alpha_rad)
            k = 1 / (2 * tan_alpha_2)

            st.success(f"Cone Angle α = {alpha_deg:.2f}°")
            st.info(f"Taper Ratio k = {k:.3f}")

            fig, ax = plt.subplots()
            X = [0, l, 0]
            Y_top = [D / 2, 0, d / 2]
            Y_bottom = [-y for y in Y_top]
            ax.plot(X, Y_top, 'r', linewidth=2)
            ax.plot(X, Y_bottom, 'r', linewidth=2)
            ax.fill_between(X, Y_top, Y_bottom, color='orange', alpha=0.3)
            ax.set_title("Cone Profile")
            ax.set_xlabel("Length (mm)")
            ax.set_ylabel("Radius (mm)")
            ax.axis('equal')
            ax.grid(True)
            st.pyplot(fig)

# ========== Support Angle ==========
with tab2:
    a = st.number_input("Tool Tip Radius r (mm)", value=0.4)
    alpha_deg = st.number_input("Cone Angle α (degrees)", value=30.0)
    support_angle = alpha_deg / 2
    st.success(f"Support Angle ≈ {support_angle:.2f}°")

    st.markdown("📌 This angle is used to tilt the compound rest on a lathe.")

# ========== Cutting Speed & Feed ==========
with tab3:
    n = st.number_input("Spindle Speed (rpm)", value=600)
    D_cutter = st.number_input("Workpiece Diameter (mm)", value=50.0)
    f = st.number_input("Feed Rate (mm/rev)", value=0.2)

    V = (math.pi * D_cutter * n) / 1000
    feed_mm_min = f * n

    st.info(f"Cutting Speed V = {V:.2f} m/min")
    st.info(f"Feed = {feed_mm_min:.2f} mm/min")

# ========== 3D Cone View ==========
with tab4:
    st.markdown("### 🧱 3D View of Cone")
    show_3d = st.button("🔄 Generate 3D Cone")
    if show_3d:
        steps = 50
        height = l
        r1 = D / 2
        r2 = d / 2
        theta = [2 * math.pi * i / steps for i in range(steps)]
        X = []
        Y = []
        Z = []
        for i in range(steps):
            X.append(r1 * math.cos(theta[i]))
            Y.append(r1 * math.sin(theta[i]))
            Z.append(0)
        for i in range(steps):
            X.append(r2 * math.cos(theta[i]))
            Y.append(r2 * math.sin(theta[i]))
            Z.append(height)

        fig3d = go.Figure(data=[go.Mesh3d(x=X, y=Y, z=Z, opacity=0.5, color='orange')])
        fig3d.update_layout(scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
        ), title="3D Cone Model")
        st.plotly_chart(fig3d)
