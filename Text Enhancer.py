# Install Libraries
!pip install fastapi uvicorn pyngrok streamlit groq pydantic requests python-dotenv

# Set API Keys
import os
from pyngrok import ngrok
os.environ["GROQ_API_KEY"] = "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"
ngrok.set_auth_token("2z0Oqv0tD166fELGCHwV2gLZwq1_2G2zUQRSs6C27k9vdzxwq")
print("Key Loaded:", os.getenv("GROQ_API_KEY")[:10], "...")

# Create Project Structure
import os
folders = ["app", "app/services", "app/utils"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# LLM Service
with open("app/services/llm_service.py", "w") as f:
    f.write("""
import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
PROMPTS = {
    "improve": \"\"\"Rewrite the following text to be clear, concise, and professional.
- Fix grammar and sentence structure
- Improve readability
- Keep original meaning unchanged
Return only the improved version.
Text:\"\"\",
    "summarize": \"\"\"Summarize the following text into key points.
- Keep it concise and informative
- Use bullet points if needed
- Focus on important information only
Text:\"\"\",
    "ideas": \"\"\"Generate exactly 5 high-quality, practical, and creative ideas.
Each idea must:
- Have a short title
- Include 1-2 line explanation
- Be realistic and actionable
Format strictly as:
1. Title - explanation
2. Title - explanation
3. Title - explanation
4. Title - explanation
5. Title - explanation
Text:\"\"\"
}
def generate_response(text: str, action: str) -> str:
    print("DEBUG INPUT:", text, action)
    if action not in PROMPTS:
        raise ValueError("Invalid action")
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    full_prompt = f"{PROMPTS[action]}\\n\\n{text.strip()}"
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI writing assistant. Provide structured and high-quality outputs."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.6
        )
        result = response.choices[0].message.content
        if not result:
            raise ValueError("Empty response from LLM")
        return result.strip()
    except Exception as e:
        print("LLM ERROR:", str(e))
        raise RuntimeError("LLM request failed")
""")

# Schemas
with open("app/schemas.py", "w") as f:
    f.write("""
from pydantic import BaseModel, Field
class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1)
    action: str
class ProcessResponse(BaseModel):
    result: str
""")

# Validator
with open("app/utils/validator.py", "w") as f:
    f.write("""
VALID_ACTIONS = {"improve", "summarize", "ideas"}
def validate_action(action: str):
    if action not in VALID_ACTIONS:
        raise ValueError(f"Action must be one of {VALID_ACTIONS}")
""")

# Routes
with open("app/routes.py", "w") as f:
    f.write("""
from fastapi import APIRouter, HTTPException
from app.schemas import ProcessRequest, ProcessResponse
from app.services.llm_service import generate_response
from app.utils.validator import validate_action
router = APIRouter()
@router.post("/process", response_model=ProcessResponse)
def process_text(request: ProcessRequest):
    try:
        action = request.action.strip().lower()
        text = request.text.strip()
        validate_action(action)
        print("ACTION:", action)
        result = generate_response(text, action)
        return ProcessResponse(result=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
""")

# Main App
with open("app/main.py", "w") as f:
    f.write("""
from fastapi import FastAPI
from app.routes import router
app = FastAPI(title="AI Text Enhancer API")
app.include_router(router)
""")

# Test LLM
from app.services.llm_service import generate_response
print(generate_response(
    "I want to build a startup but I don't know where to start",
    "ideas"
))

# Run Backend + NGROK
import threading
import uvicorn
from pyngrok import ngrok
import time
PORT = 8001
def run():
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)
threading.Thread(target=run, daemon=True).start()
time.sleep(3)
public_url = ngrok.connect(PORT)
base_url = public_url.public_url
print("API URL:", base_url)
print("Docs:", base_url + "/docs")
print("Process:", base_url + "/process")

# Test API
import requests
url = base_url + "/process"
res = requests.post(url, json={
    "text": "I want to build a startup but I don't know where to start",
    "action": "ideas"
})
print(res.json())

# UI (Streamlit)
with open("ui.py", "w") as f:
    f.write("""
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
""")

# Run Streamlit
import subprocess
from pyngrok import ngrok
subprocess.Popen(["streamlit", "run", "ui.py"])
ui_url = ngrok.connect(8501)
print("UI URL:", ui_url.public_url)
