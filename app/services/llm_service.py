import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
PROMPTS = {
    "improve": """Rewrite the following text to be clear, concise, and professional.
- Fix grammar and sentence structure
- Improve readability
- Keep original meaning unchanged
Return only the improved version.
Text:""",
    "summarize": """Summarize the following text into key points.
- Keep it concise and informative
- Use bullet points if needed
- Focus on important information only
Text:""",
    "ideas": """Generate exactly 5 high-quality, practical, and creative ideas.
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
Text:"""
}
def generate_response(text: str, action: str) -> str:
    print("DEBUG INPUT:", text, action)
    if action not in PROMPTS:
        raise ValueError("Invalid action")
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    full_prompt = f"{PROMPTS[action]}\n\n{text.strip()}"
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