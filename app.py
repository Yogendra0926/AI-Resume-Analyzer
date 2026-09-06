import streamlit as st
import tempfile
import os
from Resume import load_resume, split_text, analyze_resume

# Page Configuration
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS for Scaled-Up Premium UI
st.markdown("""
<style>
/* Reset & Base Styles */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {background: #f4f7fb; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;}
.block-container {padding: 0 0 4rem 0; max-width: 1400px !important; margin: 0 auto;}

/* Hero Section */
.hero {
    background: radial-gradient(circle at 80% 20%, #1e3a8a 0%, #0f172a 100%);
    padding: 50px 8% 120px 8%;
    color: white;
}
.nav {display: flex; justify-content: space-between; align-items: center; margin-bottom: 70px;}
.logo-container {display: flex; align-items: center; gap: 15px;}
.logo-icon {background: #3b82f6; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;}
.logo-text {font-size: 26px; font-weight: 800; line-height: 1.1;}
.tag {font-size: 14px; color: #94a3b8; font-weight: 500;}
.navlinks {display: flex; gap: 40px; color: #cbd5e1; font-size: 16px; font-weight: 500;}
.navlinks span {display: flex; align-items: center; gap: 8px; cursor: pointer; transition: 0.2s;}
.navlinks span:hover {color: white;}

.hero-grid {display: flex; justify-content: space-between; align-items: center; max-width: 1300px; margin: auto;}
.hero-left {max-width: 650px;}
.hero-title {font-size: 64px; font-weight: 800; line-height: 1.15; margin-bottom: 22px;}
.hero-title span {color: #60a5fa;}
.hero-text {font-size: 20px; color: #94a3b8; line-height: 1.6; max-width: 550px; margin-bottom: 50px;}

/* Hero Features */
.features {display: flex; gap: 30px;}
.feature {display: flex; align-items: center; gap: 15px;}
.feature-icon {width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;}
.fi-1 {background: #1e1b4b; color: #818cf8;}
.fi-2 {background: #172554; color: #a78bfa;}
.fi-3 {background: #0f172a; color: #60a5fa; border: 1px solid #1e293b;}
.feature b {font-size: 16px; font-weight: 600; display: block;}
.feature small {color: #94a3b8; font-size: 13px;}

/* Hero Right Graphic */
.hero-right {position: relative; width: 500px; height: 350px; display: flex; justify-content: flex-end;}
.hero-card {width: 320px; height: 400px; background: #ffffff; border-radius: 20px; position: absolute; top: -40px; right: 50px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); padding: 30px;}
.hc-header {display: flex; align-items: center; gap: 15px; margin-bottom: 30px;}
.hc-avatar {width: 55px; height: 55px; border-radius: 50%; background: #bfdbfe;}
.hc-lines div {height: 8px; background: #e2e8f0; border-radius: 5px; margin-bottom: 10px;}
.floating-box {position: absolute; right: -30px; top: 80px; background: #1e1b4b; border-radius: 14px; padding: 22px 30px; border: 1px solid #312e81; color: #e0e7ff; font-size: 15px; line-height: 2.2; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);}
.floating-box span {color: #a5b4fc; font-weight: bold; margin-right: 8px;}
.quote {position: absolute; right: -50px; bottom: 20px; font-style: italic; color: #cbd5e1; font-size: 15px; text-align: right;}

/* Upload Section */
.upload-container {max-width: 1300px; margin: -60px auto 0 auto; padding: 0 20px; position: relative; z-index: 10;}
.upload-box {background: white; border-radius: 24px; padding: 40px; box-shadow: 0 10px 30px -5px rgba(0,0,0,0.08); border: 1px dashed #cbd5e1;}
[data-testid="stFileUploader"] {border: 2px dashed #cbd5e1; border-radius: 16px; padding: 40px; background: #f8fafc; text-align: center;}
[data-testid="stFileUploader"] section {background: transparent;}
[data-testid="stFileUploader"] label {color: #0f172a!important; font-weight: 700; font-size: 22px;}
[data-testid="stFileUploader"] small {color: #64748b!important; font-size: 16px;}
[data-testid="stFileUploader"] button {background: #3b82f6; color: white; border-radius: 10px; font-weight: 600; padding: 10px 20px;}

/* File Card */
.file-card {background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 25px; margin-bottom: 20px; display: flex; align-items: center; gap: 20px;}
.pdf-icon {background: #ef4444; color: white; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2);}
.file-info {flex-grow: 1;}
.file-name {font-weight: 700; color: #0f172a; font-size: 18px; margin-bottom: 4px;}
.file-size {font-size: 15px; color: #64748b;}
.success-icon {color: #10b981; font-size: 20px; background: #d1fae5; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; border-radius: 50%;}

/* Analyze Button */
.stButton button {width: 100%; border: none; border-radius: 14px; background: linear-gradient(90deg, #6366f1, #a855f7); color: white; font-size: 22px; font-weight: 700; padding: 22px; transition: all 0.3s ease; box-shadow: 0 10px 20px -5px rgba(168, 85, 247, 0.4);}
.stButton button:hover {transform: translateY(-3px); box-shadow: 0 15px 25px -5px rgba(168, 85, 247, 0.6);}

/* Analysis Output Layout */
.analysis-wrapper {max-width: 1300px; margin: 40px auto; padding: 0 20px;}
.analysis-card {background: white; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; overflow: hidden;}
.ah-header {display: flex; justify-content: space-between; align-items: center; padding: 30px 40px; border-bottom: 1px solid #f1f5f9; background: #f8fafc;}
.ah-left {display: flex; align-items: center; gap: 20px;}
.bot-icon {background: #dbeafe; color: #2563eb; font-size: 32px; width: 65px; height: 65px; border-radius: 16px; display: flex; align-items: center; justify-content: center;}
.ah-title {font-size: 26px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0;}
.ah-sub {color: #64748b; font-size: 16px; margin: 0;}
.ah-right {text-align: right; color: #64748b; font-size: 15px;}

/* Formatting the Markdown Results to fit the theme */
.result-content {padding: 40px; color: #334155; line-height: 1.8; font-size: 17px;}
.result-content h1, .result-content h2, .result-content h3 {color: #0f172a; font-weight: 800; border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-top: 35px; margin-bottom: 20px;}
.result-content h1:first-child, .result-content h2:first-child {margin-top: 0;}
.result-content ul {background: #f8fafc; padding: 30px 30px 30px 50px; border-radius: 16px; border: 1px solid #f1f5f9; margin-bottom: 25px;}
.result-content li {margin-bottom: 12px;}
.result-content strong {color: #1e293b;}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="nav">
        <div class="logo-container">
            <div class="logo-icon">📄</div>
            <div>
                <div class="logo-text">AI Resume Analyzer</div>
                <div class="tag">Smart Insights for a Brighter Career</div>
            </div>
        </div>
        <div class="navlinks">
            <span>🏠 Home</span>
            <span>📊 Analyze</span>
            <span>💡 About</span>
            <span>👤 Contact</span>
        </div>
    </div>
    <div class="hero-grid">
        <div class="hero-left">
            <div class="hero-title">Turn Your Resume<br>Into <span>Opportunities</span></div>
            <div class="hero-text">Get AI-powered insights on your skills, strengths, weaknesses, improvements and the best career roles.</div>
            <div class="features">
                <div class="feature"><div class="feature-icon fi-1">⚡</div><div><b>Fast Analysis</b><small>Get results in seconds</small></div></div>
                <div class="feature"><div class="feature-icon fi-2">🎯</div><div><b>Actionable Insights</b><small>Improve your profile</small></div></div>
                <div class="feature"><div class="feature-icon fi-3">📊</div><div><b>Career Guidance</b><small>Find the right roles</small></div></div>
            </div>
        </div>
        <div class="hero-right">
            <div class="hero-card">
                <div class="hc-header">
                    <div class="hc-avatar"></div>
                    <div style="flex-grow:1;">
                        <div style="height:10px; width:70%; background:#cbd5e1; border-radius:5px; margin-bottom:10px;"></div>
                        <div style="height:8px; width:45%; background:#e2e8f0; border-radius:5px;"></div>
                    </div>
                </div>
                <div class="hc-lines">
                    <div style="width:100%;"></div>
                    <div style="width:85%;"></div>
                    <div style="width:95%;"></div>
                    <div style="width:50%; margin-bottom:30px;"></div>
                    <div style="width:100%;"></div>
                    <div style="width:90%;"></div>
                    <div style="width:80%;"></div>
                </div>
            </div>
            <div class="floating-box">
                <span>☑</span> Skills <br>
                <span>☑</span> Strengths <br>
                <span>☑</span> Improvements <br>
                <span>✦</span> Best Job Roles <br>
                <span>✦</span> Resume Score
            </div>
            <div class="quote">
                "A better resume<br>opens better doors."<br>
                <span style="color:#60a5fa; font-weight:bold;">—</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown('<div class="upload-container"><div class="upload-box">', unsafe_allow_html=True)
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"], help="Drag and drop your file here or click to browse")

with col2:
    if uploaded_file is not None:
        st.markdown(f"""
        <div class="file-card">
            <div class="pdf-icon">PDF</div>
            <div class="file-info">
                <div class="file-name">{uploaded_file.name}</div>
                <div class="file-size">{uploaded_file.size / 1024:.0f} KB</div>
            </div>
            <div class="success-icon">✓</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Analyze Resume", use_container_width=True):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_file_path = temp_file.name
            
            try:
                # NEW DETAILED PROGRESS/LOADING ANIMATION
                with st.status("🤖 **AI is analyzing your resume. Please wait...**", expanded=True) as status:
                    st.write("📄 Extracting text from PDF...")
                    docs = load_resume(temp_file_path)
                    
                    st.write("⚙️ Processing and chunking data...")
                    chunks = split_text(docs)
                    
                    st.write("🎯 Evaluating skills against industry standards...")
                    result = analyze_resume(chunks)
                    
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    
                st.session_state["resume_result"] = result
            except Exception as e:
                st.error("An error occurred while analyzing the resume.")
                st.error(str(e))
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

st.markdown('</div></div>', unsafe_allow_html=True)

# Analysis Results Section
if "resume_result" in st.session_state:
    st.markdown("""
    <div class="analysis-wrapper">
        <div class="analysis-card">
            <div class="ah-header">
                <div class="ah-left">
                    <div class="bot-icon">🤖</div>
                    <div>
                        <h3 class="ah-title">AI Resume Analysis</h3>
                        <p class="ah-sub">Here's a detailed analysis of your resume based on industry standards and recruiter insights.</p>
                    </div>
                </div>
                <div class="ah-right">
                    <span style="color:#10b981; font-weight:700; font-size:16px;">✓ Analysis Complete</span><br>
                    Generated successfully
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Display Backend Markdown dynamically inside the styled container
    st.markdown(f'<div class="result-content">{st.session_state["resume_result"]}</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)