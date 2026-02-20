import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. UI ENGINE (NO GAPS / NO EMPTY BOXES) ---
st.set_page_config(page_title="NeuroPlan AI | Final", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% 50%, #0a0a0a 0%, #000000 100%); }
    .login-box {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 40px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        text-align: center;
        margin-top: -30px;
    }
    .brand-title {
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin: 0 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ROBUST AI INITIALIZATION (FIXED) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'xp' not in st.session_state: st.session_state.xp = 0

def init_neuro_engine():
    try:
        # API Key ని సరిగ్గా కాన్ఫిగర్ చేయడం
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("API Key missing in Streamlit Secrets!")
            return None
            
        genai.configure(api_key=api_key)
        
        # మోడల్ నేమ్ చెక్ చేయడం (1.5-flash లేదా pro)
        # ఇక్కడ NotFound ఎర్రర్ రాకుండా ఉండటానికి 'models/' ప్రిఫిక్స్ వాడుతున్నాను
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Engine Failure: {str(e)}")
        return None

model = init_neuro_engine()

# --- 3. LOGIN INTERFACE ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 class="brand-title">NeuroPlan AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#D4AF37; letter-spacing:3px;">NEURAL LINK v4.0.2</p>', unsafe_allow_html=True)
        
        user_id = st.text_input("SCHOLAR_ID", placeholder="Enter Identity")
        token = st.text_input("ACCESS_TOKEN", type="password", placeholder="••••••••")
        
        if st.button("AUTHORIZE MISSION"):
            if user_id and token == "ai123":
                with st.spinner("Decoding Neural Pathways..."):
                    time.sleep(1.5)
                    st.session_state.auth = True
                    st.rerun()
            else:
                st.error("Access Denied.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. DASHBOARD ---
else:
    st.sidebar.markdown(f"## 🏆 Level {int(st.session_state.xp // 100) + 1}")
    if st.sidebar.button("Log Out"):
        st.session_state.auth = False
        st.rerun()

    st.markdown("### 🏛️ Operational Dashboard")
    
    c1, c2, c3 = st.columns(3)
    subs = c1.multiselect("Subjects", ["Law", "Physics", "Computer Science"])
    target_date = c2.date_input("Deadline", datetime.now() + timedelta(days=7))
    intensity = c3.select_slider("Intensity", ["Sustain", "Optimized", "Overdrive"])

    frictions = st.text_area("Friction Points", placeholder="Where is your focus failing?")

    if st.button("EXECUTE ANALYSIS"):
        if model and subs:
            days = (target_date - datetime.now().date()).days
            with st.status("🧠 Consulting Neural Engine..."):
                try:
                    # AI కి పంపే ప్రాంప్ట్
                    prompt = f"Expert study plan for {subs}. Focus: {frictions}. Days: {days}. Mode: {intensity}."
                    response = model.generate_content(prompt)
                    st.markdown("##### 📜 Strategy Protocol")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Generation Failed: {str(e)}")
        else:
            st.warning("Ensure subjects and API Key are ready.")

    st.divider()
    done = st.multiselect("Achievements:", ["Deep Work", "Weak Area Drill", "Review"])
    st.session_state.xp = len(done) * 34
    st.progress(st.session_state.xp / 100, text=f"Progress: {int(st.session_state.xp)}%")
