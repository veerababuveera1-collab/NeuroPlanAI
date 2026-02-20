import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. THE ARCHITECT'S UI ENGINE ---
st.set_page_config(
    page_title="NeuroPlan AI | Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to eliminate the "Empty Box" and refine the aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 50%, #111111 0%, #000000 100%);
    }

    /* Professional Card without the top blank space */
    .login-box {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 40px;
        border: 1px solid rgba(212, 175, 55, 0.15);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        text-align: center;
        margin-top: -50px; /* Pulls the card up to eliminate visual gaps */
    }

    .brand-title {
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem !important;
        font-weight: 900;
        letter-spacing: -3px;
        margin: 0 !important; /* Removes default margins causing the box effect */
        padding: 0 !important;
    }

    .badge {
        font-family: 'JetBrains Mono', monospace;
        color: #D4AF37;
        font-size: 0.7rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 10px;
        opacity: 0.7;
    }

    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        height: 50px !important;
        width: 100%;
        margin-top: 20px;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }

    /* Cleaner Input Styling */
    div[data-baseweb="input"] {
        background-color: rgba(0,0,0,0.5) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC & AUTH ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 0

def get_model():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except: return None

model = get_model()

# --- 3. THE REFINED LOGIN ---
if not st.session_state.auth:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    
    with col:
        # We put the HTML brand tags INSIDE the same block to avoid "Empty Boxes"
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 class="brand-title">NeuroPlan AI</h1>', unsafe_allow_html=True)
        st.markdown('<div class="badge">Neural Link Active // v4.0.2</div>', unsafe_allow_html=True)
        
        user = st.text_input("SCHOLAR_ID", placeholder="Identity...")
        key = st.text_input("ACCESS_TOKEN", type="password", placeholder="••••••••")
        
        if st.button("AUTHORIZE MISSION"):
            if user and key == "ai123":
                with st.spinner("Synchronizing..."):
                    time.sleep(1.5)
                    st.session_state.auth = True
                    st.rerun()
            else:
                st.toast("Invalid Token", icon="🚫")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. THE COMMAND CENTER ---
else:
    st.sidebar.markdown(f"## 🏆 Level {int(st.session_state.xp // 100) + 1}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.markdown("### 🏛️ Operational Dashboard")
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        subs = c1.multiselect("Subjects", ["Mathematics", "Code", "Physics", "Law"])
        date = c2.date_input("Deadline", datetime.now() + timedelta(days=7))
        mode = c3.select_slider("Intensity", ["Sustain", "Optimized", "Overdrive"])

    weakness = st.text_area("Friction Points", placeholder="Where is your focus failing?")

    if st.button("EXECUTE ANALYSIS"):
        if model and subs:
            days = (date - datetime.now().date()).days
            with st.status("🧠 Consulting Neural Engine..."):
                prompt = f"Expert study plan for {subs} focusing on {weakness}. Days: {days}. Mode: {mode}."
                response = model.generate_content(prompt)
                st.markdown("##### 📜 Strategy Protocol")
                st.write(response.text)
        else:
            st.warning("Configuration incomplete.")

    # XP System
    st.divider()
    done = st.multiselect("Milestones:", ["Deep Work", "Weak Point Drill", "Review"])
    st.session_state.xp = len(done) * 34
    st.progress(st.session_state.xp / 100, text=f"Progress: {int(st.session_state.xp)}%")
