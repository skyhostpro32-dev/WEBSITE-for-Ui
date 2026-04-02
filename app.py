import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# 💜 GLOBAL CSS (FINAL CLEAN UI)
# =========================
st.markdown("""
<style>

/* ❌ REMOVE STREAMLIT UI */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
footer:after {content: ""; display: none;}

/* 🌈 BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe) !important;
}

/* CENTER LOGIN */
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
}

/* GLASS CARD */
.login-card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(12px);
    padding: 30px;
    border-radius: 20px;
    width: 100%;
    max-width: 350px;
    box-shadow: 0 10px 30px rgba(139,92,246,0.2);
    text-align: center;
}

/* TITLE */
.login-title {
    font-size: 24px;
    font-weight: 700;
    color: #5b21b6;
    margin-bottom: 20px;
}

/* INPUT */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid #ddd6fe;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 10px;
    padding: 10px;
}

/* DASHBOARD TITLE */
.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #5b21b6;
}

/* IMAGE STYLE */
.stImage {
    border-radius: 12px;
    border: 1px solid #ddd6fe;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .login-card {
        padding: 20px;
        border-radius: 15px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# =========================
# DEMO USERS
# =========================
USERS = {
    "admin": "1234"
}

# =========================
# 🔐 LOGIN PAGE
# =========================
def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown('<div class="login-title">🔐 Welcome Back</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🧑‍💻 DASHBOARD
# =========================
def dashboard():
    st.markdown('<div class="main-title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

    st.markdown(f"👋 Welcome, **{st.session_state.user}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])
    tool = st.selectbox("Select Tool", ["Background Change", "Enhance Image"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Original")

        # 🎨 Background Change
        if tool == "Background Change":
            color_hex = st.color_picker("Pick Color", "#8b5cf6")
            color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

            if st.button("Apply"):
                img_array = np.array(image)
                gray = np.mean(img_array, axis=2)
                mask = gray > 200
                img_array[mask] = color
                result = Image.fromarray(img_array)

                with col2:
                    st.image(result, caption="Result")

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "bg.png")

        # ✨ Enhance
        elif tool == "Enhance Image":
            strength = st.slider("Sharpness", 1, 5, 2)

            if st.button("Enhance"):
                result = image
                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

                with col2:
                    st.image(result, caption="Result")

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "enhanced.png")

    else:
        st.info("Upload an image to start")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
