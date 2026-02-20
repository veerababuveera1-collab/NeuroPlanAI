import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. PAGE CONFIG & PREMIUM THEME ---
st.set_page_config(page_title="AI Study Planner | V2.0", page_icon="⚡", layout="wide")

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

    .title-text {
        color: #D4AF37;
        font-family: 'Courier New', monospace;
        font-size: 3rem !important;
        font-weight: 900;
        letter-spacing: -2px;
        text-transform: uppercase;
    }

    /* Subtitle Terminal Style */
    .terminal-sub {
        color: #555;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        margin-bottom: 30px;
        border-right: 2px solid #D4AF37;
        width: fit-content;
        padding-right: 5px;
    }

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
        box-shadow: 0 0 15px #D4AF37;
    }

    /* XP Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #D4AF37 !important;
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
    st.error("🔑 AI Key Missing. Please check secrets.toml")

# --- 4. LOGIN SCREEN (THEMED) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="title-text">CORE_LINK V2</h1>', unsafe_allow_html=True)
        st.markdown('<div class="terminal-sub">SYSTEM STATUS: READY_TO_LOAD...</div>', unsafe_allow_html=True)
        
        user = st.text_input("AUTHORIZED_ID", placeholder="Enter ID")
        pwd = st.text_input("PASS_KEY", type="password", placeholder="••••••••")
        
        if st.button("EXECUTE LOGIN"):
            if user and pwd == "ai123":
                with st.spinner("Decrypting Access Protocols..."):
                    time.sleep(1.5)
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.error("🚨 ACCESS_DENIED: UNAUTHORIZED_KEY")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. DASHBOARD (POST-LOGIN) ---
else:
    # Top Stats Bar
    st.markdown(f"### ⚡ Welcome back, {datetime.now().strftime('%H:%M')} | Level: {int(st.session_state.xp // 100) + 1}")
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ MODES")
        st.radio("View", ["Daily Plan", "Performance", "Neural Tips"])
        if st.button("TERMINATE"):
            st.session_state.logged_in = False
            st.rerun()

    # Main Config
    with st.container():
        st.markdown("#### 🛠️ SCRIPT_PARAMETERS")
        c1, c2, c3 = st.columns(3)
        with c1:
            subs = st.multiselect("Subjects", ["Mathematics", "Physics", "Computer Science", "Biology"])
        with c2:
            deadline = st.date_input("Deadline", datetime.now() + timedelta(days=7))
        with c3:
            mode = st.select_slider("Mode", ["Power-Save", "Standard", "Overdrive"])

    bottleneck = st.text_input("Specific Cognitive Bottleneck (Weak Area)", placeholder="e.g. Calculus, Memory Leak Detection")

    if st.button("GENERATE NEURAL STRATEGY"):
        days = (deadline - datetime.now().date()).days
        with st.status("🧠 Consulting Neural Engine...", expanded=True) as status:
            prompt = f"Student studying {subs} with weakness in {bottleneck}. Exam in {days} days. Mode: {mode}. Give a 3-step high-impact study plan."
            try:
                response = model.generate_content(prompt)
                status.update(label="STRATEGY_DECODED", state="complete")
                
                # Dynamic Results
                res_col, log_col = st.columns([2, 1])
                with res_col:
                    st.markdown("##### 📜 THE PROTOCOL")
                    st.info(response.text)
                
                with log_col:
                    st.markdown("##### 📈 METRICS")
                    st.metric("Time Remaining", f"{days} Days")
                    st.metric("Success Probability", "89%")
            except:
                st.error("AI node failed to respond.")

    # XP Section
    st.markdown("---")
    st.markdown("#### 🏆 PROGRESS_TRACKER")
    p1, p2, p3 = st.columns(3)
    if p1.checkbox("Sprint 01: Focus"): st.session_state.xp += 33
    if p2.checkbox("Sprint 02: Practice"): st.session_state.xp += 33
    if p3.checkbox("Sprint 03: Review"): st.session_state.xp += 34

    st.progress(st.session_state.xp % 100 / 100, text=f"Daily Quota: {int(st.session_state.xp % 101)}%")
    
    if st.session_state.xp >= 100:
        st.balloons()
