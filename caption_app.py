import streamlit as st
from openai import OpenAI
import json
import os
import hashlib

st.set_page_config(
    page_title="Ansah Coaching AI Caption Generator",
    page_icon="✍️",
    layout="wide"
)

client = OpenAI()
USER_FILE = "users.json"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "credits" not in st.session_state:
    st.session_state.credits = 10


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password):
    users = load_users()

    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)
    return True


def login_user(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)


st.markdown("""
<style>
.stApp {
    background-color: #F8F3EA;
    color: #000052;
}

header[data-testid="stHeader"] {
    display: none;
}

div[data-testid="stToolbar"] {
    display: none;
}

.block-container {
    padding-top: 2rem;
    max-width: 950px;
}

.logo-box {
    text-align: center;
    margin-bottom: 25px;
}

.brand-logo {
    font-size: 42px;
    font-weight: 800;
    color: #000052;
}

.brand-gold {
    color: #ad9551;
}

.subtitle {
    text-align: center;
    color: #3f3f66;
    font-size: 18px;
    margin-top: -10px;
}

.stButton > button {
    width: 100%;
    background-color: #ad9551;
    color: white;
    border-radius: 14px;
    height: 52px;
    font-weight: 700;
    border: none;
}

.stButton > button:hover {
    background-color: #000052;
    color: white;
}

.stDownloadButton > button {
    width: 100%;
    background-color: #000052;
    color: white;
    border-radius: 14px;
    height: 48px;
    font-weight: 700;
}

.caption-card {
    background-color: #ffffff;
    border: 1px solid #eadfcd;
    border-left: 6px solid #ad9551;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 82, 0.06);
    color: #000052;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="logo-box">
    <div class="brand-logo">Ansah <span class="brand-gold">Coaching</span></div>
    <div class="subtitle">Premium caption generation for creators, coaches, and businesses</div>
</div>
""", unsafe_allow_html=True)


if not st.session_state.logged_in:
    with st.container(border=True):
        st.subheader("Welcome Back")

        auth_mode = st.radio(
            "Choose an option",
            ["Login", "Create Account"],
            horizontal=True
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if auth_mode == "Create Account":
            if st.button("Create Account"):
                if not username or not password:
                    st.warning("Please enter a username and password.")
                elif create_user(username, password):
                    st.success("Account created. You can now log in.")
                else:
                    st.error("That username already exists.")

        if auth_mode == "Login":
            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

else:
    col_a, col_b = st.columns([3, 1])

    with col_a:
        st.markdown(f"### Welcome, {st.session_state.username}")
        st.info(f"Credits remaining: {st.session_state.credits}")

    with col_b:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    with st.container(border=True):
        st.subheader("Create Viral Captions")

        topic = st.text_input(
            "What is your post about?",
            placeholder="Example: digital marketing, meal plans, real estate"
        )

        col1, col2 = st.columns(2)

        with col1:
            caption_count = st.slider("How many captions?", 5, 50, 20)

            tone = st.selectbox(
                "Choose a tone",
                ["Catchy", "Emotional", "Professional", "Funny", "Luxury", "Bold", "Inspirational"]
            )

        with col2:
            platform = st.selectbox(
                "Choose platform",
                ["Instagram", "TikTok", "Facebook", "LinkedIn", "X/Twitter", "YouTube Shorts"]
            )

            hook_style = st.selectbox(
                "Hook Style",
                ["Question", "Bold Statement", "Story", "Controversial", "Educational"]
            )

        if st.session_state.credits <= 0:
            st.error("You've used all your free credits for today.")
            st.stop()

        generate = st.button("Generate Captions")

    if generate:
        if not topic:
            st.warning("Please enter a topic first.")
        else:
            st.session_state.credits -= 1

            with st.spinner("Crafting viral captions for you..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=f"""
Write {caption_count} social media captions about: {topic}.

Platform: {platform}
Tone: {tone}
Hook style: {hook_style}

Rules:
- Number each caption from 1 to {caption_count}
- Keep each caption short and easy to read
- Each caption should be one paragraph only
- Include relevant hashtags at the end of each caption
- Do not use quotation marks around the captions
- Separate each caption with a blank line
"""
                )

            captions_output = response.output_text.strip()

            st.markdown("---")
            st.subheader("Copy All Captions")

            st.text_area(
                label="One-click copy block",
                value=captions_output,
                height=420,
                label_visibility="collapsed"
            )

            st.download_button(
                label="Download Captions",
                data=captions_output,
                file_name=f"{topic.replace(' ', '_')}_captions.txt",
                mime="text/plain"
            )

            st.markdown("---")
            st.subheader("Preview Captions")

            captions = captions_output.split("\n\n")

            for cap in captions:
                if cap.strip():
                    st.markdown(
                        f'<div class="caption-card">{cap.strip()}</div>',
                        unsafe_allow_html=True
                    )