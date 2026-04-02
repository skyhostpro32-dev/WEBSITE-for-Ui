import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# 💜 CSS
# =========================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe) !important;
}

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
}

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

.login-title {
    font-size: 22px;
    font-weight: 700;
    color: #5b21b6;
    margin-bottom: 15px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 10px;
    padding: 10px;
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

if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "1234"}  # default user

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# =========================
# 🔐 AUTH UI
# =========================
def auth_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # Toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.auth_mode = "login"
    with col2:
        if st.button("Signup"):
            st.session_state.auth_mode = "signup"

    mode = st.session_state.auth_mode

    st.markdown(f'<div class="login-title">{"🔐 Login" if mode=="login" else "📝 Signup"}</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # =========================
    # LOGIN
    # =========================
    if mode == "login":
        if st.button("Login Now"):
            if username in st.session_state.users_db and st.session_state.users_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # =========================
    # SIGNUP
    # =========================
    else:
        if st.button("Create Account"):
            if username in st.session_state.users_db:
                st.error("User already exists")
            elif username == "" or password == "":
                st.warning("Enter valid details")
            else:
                st.session_state.users_db[username] = password
                st.success("Account created! Please login")
                st.session_state.auth_mode = "login"

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🧑‍💻 DASHBOARD
# =========================
def dashboard():
    st.markdown(f"## 👋 Welcome, {st.session_state.user}")

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
                    st.image(result)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "bg.png")

        else:
            strength = st.slider("Sharpness", 1, 5, 2)

            if st.button("Enhance"):
                result = image
                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

                with col2:
                    st.image(result)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "enhanced.png")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
