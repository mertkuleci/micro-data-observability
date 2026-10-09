import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_anomalies(anomalies_summary):
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not defined."

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
You are a Senior Data Engineer and Data Quality Analyst. Analyze the following data anomaly detection report and provide a concise, high-quality technical analysis.

Anomaly Report:
{anomalies_summary}

Requirements:
- Keep the response concise, clear, and professional.
- Use exactly these 2 sections:
  1. **Possible Root Cause:** (2-3 sentences explaining why this low row count and high null rate might have happened in a data pipeline)
  2. **Recommended Action & Fix SQL:** (Provide practical investigation steps and a sample SQL query to clean or investigate bad records)
"""

    # Garanti çalışan varsayılan metin modelleri
    candidate_models = [
        "llama-3.3-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]

    # Groq API'sinden hesabınızdaki aktif metin modellerini dinamik olarak çekelim
    try:
        models_page = client.models.list()
        active_text_models = [
            m.id for m in models_page.data 
            if not any(x in m.id for x in ['whisper', 'vision', 'guard', 'safetensors'])
        ]
        if active_text_models:
            candidate_models = active_text_models + candidate_models
    except Exception:
        pass

    last_error = ""
    for model_name in candidate_models:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = str(e)
            continue

    return f"Groq API Error: {last_error}"