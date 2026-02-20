import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. THE ARCHITECT'S UI ENGINE (PREMIUM CSS) ---
st.set_page_config(
    page_title="NeuroPlan AI | Premium Edition",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@200&display=swap');

    /* Executive Obsidian Theme */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a1a 0%, #050505 100%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Modern Glassmorphism Container */
    .executive-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border-radius: 24px;
        padding: 3.5rem;
        border: 1px solid rgba(212, 175, 55, 0.12);
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9);
        text-align: center;
        max-width: 550px;
        margin: auto;
    }

    /* Typography */
    .brand-header {
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        font-weight: 800;
        letter-spacing: -4px;
        margin-bottom: 0;
    }

    .system-status {
        font-family: 'JetBrains Mono', monospace;
        color: #D4AF37;
        font-size: 0.7rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 3rem;
        opacity: 0.7;
    }

    /* Luxury Form Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #D4AF37 !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        border-radius: 12px !important;
        height: 50px;
        font-size: 1rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1) !important;
    }

    /* Call to Action Button */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        height: 55px !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 1rem;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.4);
        color: #000 !important;
    }

    /* Custom Metrics & Progress */
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: 800 !important; }
    .stProgress > div > div > div > div { background-color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND INITIALIZATION ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'xp_points' not in st.session_state: st.session_state.xp_points = 0

def init_ai():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

ai_model = init_ai()

# --- 3. THE LOGIN INTERFACE ---
if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])
    
    with col:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="brand-header">NeuroPlan AI</h1>', unsafe_allow_html=True)
        st.markdown('<div class="system-status">Neural Encryption Active // v4.0.2</div>', unsafe_allow_html=True)
        
        user_id = st.text_input("SCHOLAR_IDENTITY", placeholder="Enter ID...")
        access_key = st.text_input("SECURITY_TOKEN", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE"):
            if user_id and access_key == "ai123":
                with st.spinner("Decoding Neural Pathways..."):
                    time.sleep(2)
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.toast("Access Revoked: Invalid Token", icon="🚫")
        
        st.markdown('<p style="color:#555; font-size:0.7rem; margin-top:3rem; letter-spacing:1px;">© 2026 NEUROPLAN ENTERPRISE SYSTEMS</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. THE COMMAND DASHBOARD ---
else:
    # Sidebar Navigation & Profile
    with st.sidebar:
        st.markdown(f"## 💎 Level {int(st.session_state.xp_points // 100) + 1}")
        st.progress(st.session_state.xp_points % 100 / 100)
        st.write(f"Experience: {st.session_state.xp_points} XP")
        st.divider()
        if st.button("LOGOUT"):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown("### 🏛️ Operational Dashboard")
    
    # Configuration Panel
    with st.container():
        st.markdown("#### ⚙️ MISSION PARAMETERS")
        c1, c2, c3 = st.columns(3)
        with c1:
            active_subs = st.multiselect("Subjects", ["Mathematics", "Deep Learning", "Applied Physics", "Business Law"])
        with c2:
            deadline_date = st.date_input("Deadline", datetime.now() + timedelta(days=14))
        with c3:
            intensity_mode = st.select_slider("Intensity", ["Sustain", "Optimized", "Overdrive"])

    bottlenecks = st.text_area("Cognitive Constraints", placeholder="Specify complex topics or areas of friction...")

    if st.button("EXECUTE GENERATIVE ARCHITECTURE"):
        if not active_subs or not ai_model:
            st.warning("Ensure subjects are selected and API key is active.")
        else:
            days_to_go = (deadline_date - datetime.now().date()).days
            with st.status("🧠 Consulting Neural Engine...", expanded=True) as status:
                prompt = f"""
                You are a senior academic strategist. Design a high-yield study plan for {active_subs}.
                Focus heavily on solving these friction points: {bottlenecks}.
                Timeline: {days_to_go} days. Mode: {intensity_mode}.
                Provide a structured table and 3 tactical tips for long-term retention.
                """
                try:
                    response = ai_model.generate_content(prompt)
                    status.update(label="STRATEGY DEPLOYED", state="complete")
                    
                    res_col, stats_col = st.columns([2, 1])
                    with res_col:
                        st.markdown("##### 📜 THE PROTOCOL")
                        st.markdown(response.text)
                    
                    with stats_col:
                        st.markdown("##### 📈 ANALYTICS")
                        st.metric("Deadline Window", f"{days_to_go} Days")
                        st.metric("Cognitive Load", f"{'92%' if intensity_mode == 'Overdrive' else '65%'}")
                        st.info("💡 Pro-Tip: Active Recall sessions are most effective in your first 90 minutes.")
                except Exception as e:
                    st.error("AI Node Offline. Please check connectivity.")

    # Gamification Loop
    st.divider()
    st.markdown("#### 🏆 ACTIVE ACHIEVEMENTS")
    cols = st.columns(3)
    t1 = cols[0].checkbox("Deep Work Completed (2hr)")
    t2 = cols[1].checkbox("Weak Area Breakthrough")
    t3 = cols[2].checkbox("Daily Review Logged")
    
    # Update XP
    new_xp = sum([t1, t2, t3]) * 34
    if new_xp > st.session_state.xp_points:
        st.session_state.xp_points = new_xp
        if st.session_state.xp_points >= 100:
            st.balloons()
            st.toast("New Rank Achieved!", icon="🏅")
