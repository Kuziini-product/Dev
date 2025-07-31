import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY nu este setată. Verifică fișierul .env sau Streamlit Secrets.")

client = OpenAI(api_key=API_KEY)

def genereaza_deviz_AI(prompt_user: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ești un expert în mobilier care generează devize detaliate."},
                {"role": "user", "content": prompt_user}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Eroare la generarea devizului: {e}"