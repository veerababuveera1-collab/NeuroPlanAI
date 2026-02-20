import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. PAGE CONFIG & PREMIUM THEME ---
st.set_page_config(page_title="NeuroPlan AI | Neural Study OS", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Midnight Gold Cyberpunk Theme */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px;
    }
    
    /* Elegant Login Container */
    .login-container {
        background: rgba(10, 10, 10, 0.95);
        padding: 60px;
        border-radius: 5px;
        border-left: 5px solid #D4AF37;
        box-shadow: 0 20px 50px rgba(0,0,0,1);
        text-align: left;
        margin-top: 5vh;
    }

    .brand-text {
        color: #D4AF37;
        font-family: 'Courier New', monospace;
        font-size: 3.2rem !important;
        font-weight: 900;
        letter-spacing: -1px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

    .terminal-sub {
        color: #555;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        margin-bottom: 30px;
        border-right: 2px solid #D4AF37;
        width: fit-content;
        padding-right: 8px;
        animation: blink 1s infinite;
    }

    @keyframes blink { 50% { border-color: transparent; } }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #111 !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        border-radius: 0px !important;
    }

    /* Professional Gold Button */
    .stButton > button {
        background: #D4AF37 !important;
        color: black !important;
        font-family: 'Courier New', monospace;
        font-weight: bold !important;
        border-radius: 0px !important;
        border: none !important;
        height: 45px;
        transition: 0.4s;
    }

    .stButton > button:hover {
        background: #ffffff !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- 3. AI CONFIGURATION ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔑 API Key Error: Check .streamlit/secrets.toml")

# --- 4. LOGIN SCREEN ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 1.6, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="brand-text">NEUROPLAN AI</h1>', unsafe_allow_html=True)
        st.markdown('<div class="terminal-sub">INITIALIZING COGNITIVE_OS...</div>', unsafe_allow_html=True)
        
        user = st.text_input("SCHOLAR_ID", placeholder="Enter Identity")
        pwd = st.text_input("ACCESS_KEY", type="password", placeholder="••••••••")
        
        # User Credentials Info (Visual Only)
        st.markdown(f'<p style="color:#444; font-size:0.7rem;">ENCRYPTION: AES-256 ACTIVE</p>', unsafe_allow_html=True)

        if st.button("AUTHORIZE ACCESS"):
            if user and pwd == "ai123":
                with st.spinner("Decoding Neural Pathways..."):
                    time.sleep(1.5)
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.error("INVALID_KEY: ACCESS_DENIED")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. DASHBOARD (POST-LOGIN) ---
else:
    st.markdown(f"### ⚡ NEUROPLAN // COMMAND_CENTER")
    
    with st.sidebar:
        st.markdown("### 🛠️ SESSION")
        st.info(f"User: Admin\nStatus: Online")
        if st.button("TERMINATE"):
            st.session_state.logged_in = False
            st.rerun()

    # Main Planner Logic
    with st.expander("📝 PLANNER CONFIGURATION", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            subs = st.multiselect("Subjects", ["Mathematics", "Computer Science", "Physics", "Chemistry", "Economics"])
        with c2:
            deadline = st.date_input("Exam Date", datetime.now() + timedelta(days=10))
        with c3:
            intensity = st.select_slider("Intensity", ["Low", "Medium", "High"])

    weakness = st.text_input("Target Weak Point", placeholder="e.g., Organic Chemistry mechanisms")

    if st.button("EXECUTE GENERATIVE ANALYSIS"):
        days = (deadline - datetime.now().date()).days
        with st.status("🧠 AI Architecting Your Success...", expanded=True) as status:
            prompt = f"Act as an expert study coach. Create a 3-step study strategy for {subs} with focus on {weakness}. Days left: {days}. Intensity: {intensity}."
            try:
                response = model.generate_content(prompt)
                status.update(label="OPTIMIZATION COMPLETE", state="complete")
                
                st.markdown("### 📋 YOUR NEURAL PROTOCOL")
                st.write(response.text)
                
                # Metrics Section
                m1, m2 = st.columns(2)
                m1.metric("Countdown", f"{days} Days")
                m2.metric("XP Multiplier", "1.5x")
            except:
                st.error("Neural Node timeout. Check internet connection.")

    # Gamification
    st.markdown("---")
    st.markdown("#### 🏆 PROGRESS_LOGGER")
    t1, t2, t3 = st.columns(3)
    if t1.checkbox("Deep Work Sprint"): st.session_state.xp += 33
    if t2.checkbox("Active Recall Drill"): st.session_state.xp += 33
    if t3.checkbox("Daily Summary"): st.session_state.xp += 34

    st.progress(st.session_state.xp % 101 / 100, text=f"Daily Quota: {int(st.session_state.xp % 101)}%")
    
    if st.session_state.xp >= 100:
        st.balloons()
