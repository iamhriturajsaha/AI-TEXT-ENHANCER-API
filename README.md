# 🚀AI Text Enhancer API

A simple yet powerful AI-powered API that enhances text using Large Language Models (LLMs). Users can improve writing, summarize content or generate ideas through a single API endpoint.

## ✨ Features

| Feature | Description |
|---|---|
| ✍️ Improve Writing | Fix grammar, clarity and professionalism |
| 📄 Summarize Text | Get concise, structured summaries |
| 💡 Generate Ideas | Brainstorm creative and actionable ideas |
| ⚡ Powered by Groq | Fast inference via LLaMA 3.1 |

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Groq (LLaMA 3.1) |
| Language | Python |

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/iamhriturajsaha/AI-TEXT-ENHANCER-API.git
cd AI-TEXT-ENHANCER-API
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API key
Create a `.env` file in the project root or export the variable directly -
```bash
export GROQ_API_KEY=your_api_key_here
```

### 4. Start the backend (FastAPI)
```bash
uvicorn app.main:app --reload
```

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | Base API |
| `http://127.0.0.1:8000/docs` | Swagger/Interactive Docs |

### 5. Start the UI (Streamlit)
```bash
streamlit run ui.py
```

## 🧪 Example Requests

### ✍️ Improve Writing
**Request**
```json
{
  "text": "i want build startup but dont know how",
  "action": "improve"
}
```

**Response**
```json
{
  "result": "I want to build a startup, but I am unsure how to begin."
}
```

### 📄 Summarize Text
**Request**
```json
{
  "text": "Building a startup requires identifying a problem, researching the market, and developing a product.",
  "action": "summarize"
}
```

**Response**
```json
{
  "result": "- Identify a problem\n- Research the market\n- Develop a product"
}
```

### 💡 Generate Ideas
**Request**
```json
{
  "text": "I want to build something using AI for students",
  "action": "ideas"
}
```

**Response**
```json
{
  "result": "1. AI Study Planner – Helps students organize schedules efficiently.\n2. Smart Notes Generator – Converts lectures into structured notes.\n3. Doubt Solver Chatbot – Provides instant answers to questions.\n4. Personalized Learning Assistant – Adapts content to student needs.\n5. Exam Predictor Tool – Suggests high-priority topics before exams."
}
```

## 🧠 Design Decisions

- **Single endpoint (`/process`) -** Keeps the API simple and easy to scale with new actions.
- **Action-based prompt routing -** Each action maps to a tailored prompt for higher quality output.
- **Input validation -** Prevents empty or invalid requests from reaching the LLM.
- **Structured prompts -** Engineered for clean, consistent, production-ready output.
- **Streamlit UI -** Simulates a real SaaS product experience as a bonus deliverable.
