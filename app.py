import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. THEME & UI STYLING ---
st.set_page_config(page_title="AI Study Planner | Neural Link", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp { background: radial-gradient(circle at center, #0a0b10, #000000); }
    
    /* Login Card Glassmorphism */
    .login-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 50px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.1);
        text-align: center;
        margin-top: 50px;
    }

    .glow-text {
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800;
        margin-bottom: 0;
    }

    /* Professional Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE & AI SETUP ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'xp' not in st.session_state: st.session_state.xp = 0

# Configure Gemini AI
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("AI Engine configuration failed. Check your API Key in secrets.")

# --- 3. LOGIN SCREEN ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="glow-text">STUDY AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; letter-spacing: 2px;">NEURAL COMMAND INTERFACE</p>', unsafe_allow_html=True)
        
        user = st.text_input("Scholar Identity", placeholder="Username")
        pwd = st.text_input("Access Key", type="password", placeholder="••••••••")
        
        if st.button("INITIATE NEURAL LINK"):
            if user and pwd == "ai123": # Replace with your real auth logic
                with st.spinner("Synchronizing neural patterns..."):
                    time.sleep(1.5)
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.error("Invalid Credentials.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MAIN APPLICATION (POST-LOGIN) ---
else:
    st.sidebar.title("🚀 Navigation")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("## 🧠 Your AI Study Command Center")
    
    # User Inputs
    with st.container():
        st.subheader("🛠️ Mission Configuration")
        c1, c2 = st.columns(2)
        with c1:
            subjects = st.multiselect("Active Subjects", ["Mathematics", "Data Structures", "Quantum Physics", "Computer Science", "Biology"])
            exam_date = st.date_input("Target Exam Date", datetime.now() + timedelta(days=14))
        with c2:
            intensity = st.select_slider("Neural Intensity", ["Chill", "Optimized", "Beast Mode"])
            weak_areas = st.text_area("Cognitive Bottlenecks (Weak Topics)", placeholder="e.g. Integration, Pointers in C++")

    if st.button("ACTIVATE GENERATIVE PLAN"):
        days_left = (exam_date - datetime.now().date()).days
        
        with st.status("AI Generating Strategy...", expanded=True) as status:
            st.write("⚙️ Analyzing syllabus density...")
            
            # Gemini Prompt
            prompt = f"""
            You are a professional study architect. Create a study plan for:
            Subjects: {subjects}
            Weak Areas: {weak_areas}
            Days Left: {days_left}
            Intensity: {intensity}
            
            Provide: 
            1. A structured daily routine table.
            2. Three 'Active Recall' tips for the weak areas.
            3. A high-energy motivational quote.
            """
            
            try:
                response = model.generate_content(prompt)
                status.update(label="Strategy Optimized!", state="complete")
                
                # Layout Results
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.markdown("### 📋 AI Protocol")
                    st.write(response.text)
                
                with col_right:
                    st.markdown("### 📊 Exam Readiness")
                    st.metric("Countdown", f"{days_left} Days")
                    st.metric("Efficiency Goal", "95%")
                    st.info("💡 Pro-Tip: Your data suggests early morning sessions work best for your 'Weak Areas'.")
            
            except Exception as e:
                st.error(f"AI Connection Error: {e}")

    # --- 5. PROGRESS & XP TRACKER ---
    st.divider()
    st.subheader("🏆 XP Progression")
    
    p1, p2, p3 = st.columns(3)
    t1 = p1.checkbox("Deep Work Completed")
    t2 = p2.checkbox("Weak Area Drilled")
    t3 = p3.checkbox("Review Session Done")
    
    # Calculate XP
    done = sum([t1, t2, t3])
    st.session_state.xp = (done / 3) * 100
    
    st.progress(st.session_state.xp / 100, text=f"Level Progress: {int(st.session_state.xp)}%")
    
    if done == 3:
        st.balloons()
        st.success("Daily Mission Accomplished! +100 XP gained.")
