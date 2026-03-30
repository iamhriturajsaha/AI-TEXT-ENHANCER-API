import streamlit as st
import requests
st.set_page_config(page_title="AI Text Enhancer", layout="centered")
def set_bg():
    bg_url = "https://images.unsplash.com/photo-1636690513351-0af1763f6237?auto=format&fit=crop&w=1920&q=80"
    st.markdown(f'''
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
}}
    /* Dark overlay */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.55);
        z-index: 0;
    }}
    /* Bring content above overlay */
    [data-testid="stAppViewContainer"] > div {{
        position: relative;
        z-index: 1;
    }}
    /* Text colors */
    h1, h2, h3, h4, h5, h6, p, label {{
        color: white !important;
    }}
    /* Input boxes */
    textarea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 8px !important;
    }}
    /* Buttons */
    button[kind="primary"] {{
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
    }}
    </style>
    ''', unsafe_allow_html=True)
set_bg()

# Header
st.title("🚀 AI Text Enhancer")
st.caption("Transform your text instantly using AI")

# API URL
API_URL = "http://localhost:8001/process"

# Tabs
tab1, tab2, tab3 = st.tabs(["✍️ Improve", "📄 Summarize", "💡 Ideas"])
def process_text(text, action):
    try:
        res = requests.post(API_URL, json={
            "text": text,
            "action": action
        })
        if res.status_code == 200:
            return res.json()["result"]
        else:
            return f"Error: {res.json()}"
    except Exception as e:
        return str(e)

# TAB 1 — Improve
with tab1:
    st.subheader("Improve Writing")
    text = st.text_area("Enter your text:", key="improve")
    if st.button("Enhance Text", key="btn1"):
        if not text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Improving..."):
                result = process_text(text, "improve")
                st.markdown("### ✨ Improved Version")
                st.markdown(result)

# TAB 2 — Summarize
with tab2:
    st.subheader("Summarize Text")
    text = st.text_area("Enter your text:", key="summarize")
    if st.button("Summarize", key="btn2"):
        if not text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Summarizing..."):
                result = process_text(text, "summarize")
                st.markdown("### 📌 Summary")
                st.markdown(result)

# TAB 3 — Ideas
with tab3:
    st.subheader("Generate Ideas")
    text = st.text_area("Enter your idea/topic:", key="ideas")
    if st.button("Generate Ideas", key="btn3"):
        if not text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Generating ideas..."):
                result = process_text(text, "ideas")
                st.markdown("### 💡 Ideas")
                st.markdown(result)

# Footer
st.divider()
st.caption("Built with FastAPI + Groq LLM • Demo Project")
