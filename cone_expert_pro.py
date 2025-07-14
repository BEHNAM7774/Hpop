
import streamlit as st
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.graph_objects as go

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# ========== Page Config ==========
st.set_page_config(page_title="Cone Expert Pro", layout="centered", page_icon="🌀")

# Language and Theme
lang = st.sidebar.radio("🌐 Language / زبان", ("English", "فارسی"))
theme = st.sidebar.selectbox("🎨 Theme", ["Modern Light", "Engineering Dark"])
if theme == "Engineering Dark":
    st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

# ========== Translations ==========
texts = {
    "English": {
        "title": "🌀 Cone Expert Pro",
        "mode": "Calculation Mode",
        "mode1": "Angle from D, d, l",
        "mode2": "D/d/l from angle",
        "unit": "Unit",
        "mm": "Millimeters (mm)",
        "inch": "Inches (in)",
        "inputs": {
            "D": "Large diameter D",
            "d": "Small diameter d",
            "l": "Cone length l",
            "alpha": "Cone angle α",
            "realD": "Real measured D (optional)"
        },
        "submit": "Calculate",
        "error": "Invalid dimensions. D must be > d and l > 0.",
        "results": {
            "angle": "Cone angle α",
            "k": "Taper ratio k",
            "length": "Length l",
            "download": "📥 Download Graph",
            "error": "Measurement Error"
        },
        "extra": {
            "3d": "3D View",
            "history": "Calculation History",
            "clear": "Clear History",
            "support_tool": "Support Angle Calculator (Coming soon)",
            "feed_tool": "Feed & Speed Tool (Coming soon)"
        }
    },
    "فارسی": {
        "title": "🌀 مخروط‌یار حرفه‌ای",
        "mode": "حالت محاسبه",
        "mode1": "محاسبه زاویه از D، d، l",
        "mode2": "محاسبه D یا d یا l از زاویه",
        "unit": "واحد",
        "mm": "میلی‌متر",
        "inch": "اینچ",
        "inputs": {
            "D": "قطر بزرگ D",
            "d": "قطر کوچک d",
            "l": "طول مخروط l",
            "alpha": "زاویه مخروط α",
            "realD": "قطر واقعی D (اختیاری)"
        },
        "submit": "محاسبه",
        "error": "مقادیر نادرست هستند. D باید > d و l > ۰ باشد.",
        "results": {
            "angle": "زاویه مخروط α",
            "k": "ضریب مخروطی بودن k",
            "length": "طول l",
            "download": "📥 دانلود گراف",
            "error": "خطای ساخت"
        },
        "extra": {
            "3d": "نمای سه‌بعدی",
            "history": "تاریخچه محاسبات",
            "clear": "پاک‌کردن تاریخچه",
            "support_tool": "محاسبه زاویه ساپورت (به‌زودی)",
            "feed_tool": "محاسبه پیشروی و سرعت (به‌زودی)"
        }
    }
}
T = texts[lang]

st.title(T["title"])

# Units
unit = st.sidebar.selectbox(T["unit"], [T["mm"], T["inch"]])
unit_factor = 1.0 if unit == T["mm"] else 25.4

# Mode switch
mode = st.selectbox(T["mode"], (T["mode1"], T["mode2"]))

# Mode 1: calculate angle
if mode == T["mode1"]:
    D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0) * unit_factor
    d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0) * unit_factor
    l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0) * unit_factor
    real_D = st.number_input(T["inputs"]["realD"], min_value=0.0, value=0.0) * unit_factor

    if st.button(T["submit"]):
        if D > d and l > 0:
            delta = D - d
            tan_alpha_2 = delta / (2 * l)
            alpha_rad = math.atan(tan_alpha_2) * 2
            alpha_deg = math.degrees(alpha_rad)
            k = 1 / (2 * tan_alpha_2)

            st.success(f"🔺 {T['results']['angle']}: {alpha_deg:.2f}°")
            st.info(f"📏 {T['results']['k']}: {k:.3f}")

            if real_D > 0:
                error_percent = abs(real_D - D) / D * 100
                st.warning(f"📐 {T['results']['error']}: {error_percent:.2f}%")

            # History
            st.session_state.history.append(f"α={alpha_deg:.2f}°, D={D}, d={d}, l={l}, k={k:.3f}")

            # 2D Plot
            fig, ax = plt.subplots()
            X = [0, l, 0]
            Y_top = [D / 2, 0, d / 2]
            Y_bottom = [-y for y in Y_top]
            ax.plot(X, Y_top, 'r', linewidth=2)
            ax.plot(X, Y_bottom, 'r', linewidth=2)
            ax.fill_between(X, Y_top, Y_bottom, color='orange', alpha=0.3)
            ax.set_title(T["title"])
            ax.set_xlabel("L")
            ax.set_ylabel("Diameter")
            ax.axis('equal')
            ax.grid(True)
            st.pyplot(fig)

            # Download
            buffer = BytesIO()
            fig.savefig(buffer, format="png")
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:file/png;base64,{b64}" download="cone_graph.png">{T["results"]["download"]}</a>'
            st.markdown(href, unsafe_allow_html=True)

            # 3D view
            if st.checkbox(T["extra"]["3d"]):
                z = [0, l]
                x = [D/2, d/2]
                fig3d = go.Figure(data=[go.Cone(x=[0], y=[0], z=[0], u=[0], v=[0], w=[l],
                                                sizemode="absolute", sizeref=2)])
                fig3d.update_layout(title="Cone View (3D)", scene=dict(zaxis_title='Length'))
                st.plotly_chart(fig3d)

# Mode 2: from angle
if mode == T["mode2"]:
    alpha_deg = st.number_input(T["inputs"]["alpha"], min_value=0.1, value=30.0)
    known = st.selectbox("🔧 Known values", ["D & d", "D & l", "d & l"])

    tan_alpha_2 = math.tan(math.radians(alpha_deg / 2))

    if known == "D & d":
        D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0) * unit_factor
        d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0) * unit_factor
        if D > d:
            l = (D - d) / (2 * tan_alpha_2)
            st.success(f"📏 {T['results']['length']} = {l:.2f} {unit}")
    elif known == "D & l":
        D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0) * unit_factor
        l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0) * unit_factor
        d = D - 2 * l * tan_alpha_2
        st.success(f"📏 {T['inputs']['d']} = {d:.2f} {unit}")
    elif known == "d & l":
        d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0) * unit_factor
        l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0) * unit_factor
        D = d + 2 * l * tan_alpha_2
        st.success(f"📏 {T['inputs']['D']} = {D:.2f} {unit}")

# Calculation History
st.sidebar.subheader(T["extra"]["history"])
for h in reversed(st.session_state.history[-5:]):
    st.sidebar.markdown(f"- {h}")

if st.sidebar.button(T["extra"]["clear"]):
    st.session_state.history = []

# Placeholder links for other machining tools
st.sidebar.markdown("---")
st.sidebar.markdown(f"🧰 {T['extra']['support_tool']}")
st.sidebar.markdown(f"⚙️ {T['extra']['feed_tool']}")
