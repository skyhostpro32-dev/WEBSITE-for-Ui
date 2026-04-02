import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# =========================
# SIMPLE USER STORAGE (DEMO)
# =========================
USERS = {
    "admin": "1234",
    "user": "1234"
}

# =========================
# 💜 LOGIN PAGE
# =========================
def login_page():
    st.markdown("## 🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# =========================
# 💜 DASHBOARD
# =========================
def dashboard():
    st.markdown(f"## 👋 Welcome, {st.session_state.user}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("---")

    # Upload
    uploaded_file = st.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])

    # Tool selection
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
# MAIN ROUTER
# =========================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
