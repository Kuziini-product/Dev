import streamlit as st
from ai_generator import genereaza_deviz_AI
from deviz_exporter import export_excel, export_pdf
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path

load_dotenv()
st.set_page_config(page_title="Kuziini | Generator Devize", layout="wide")

logo_path = "Kuziini_logo_negru.png"
if Path(logo_path).exists():
    st.image(logo_path, width=250)

st.title("Kuziini | Configurator AI Devize Mobilier")

# 📊 Contor devize
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
istoric_path = output_dir / "istoric.json"
nr_devize = len(list(output_dir.glob("OF-*.json")))
st.markdown(f"📊 **Devize generate: {nr_devize}**")

# 📋 Date client
col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client")
with col2:
    telefon_client = st.text_input("Telefon client")

# 📐 Dimensiuni
st.subheader("Dimensiuni mobilier (mm)")
col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime", min_value=0)
with col2:
    latime = st.number_input("Lățime", min_value=0)
with col3:
    adancime = st.number_input("Adâncime", min_value=0)

# 🔧 Tip mobilier
tip_mobilier = st.selectbox("Tip mobilier:", [
    "Corp bază bucătărie",
    "Corp suspendat bucătărie",
    "Corp colțar bază",
    "Corp colțar suspendat",
    "Dulap dressing",
    "Comodă",
    "Poliță simplă",
    "Ansamblu bucătărie",
    "Ansamblu dressing"
])

# 🧠 Prompt
prompt = st.text_area("Descriere detaliată pentru AI")
foloseste_gpt = st.checkbox("Folosește GPT pentru rescriere prompt", value=True)

# 📎 Export după generare
def save_offer(meta, content):
    cod = meta["cod_oferta"]
    json_path = output_dir / f"{cod}.json"
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)
    export_pdf(content, str(output_dir / cod))
    export_excel(content, str(output_dir / cod))

# ▶️ Generare ofertă
if st.button("Generează ofertă"):
    if not nume_client or inaltime == 0 or latime == 0 or adancime == 0:
        st.warning("Completează toate câmpurile înainte de generare.")
    else:
        with st.spinner("🧠 Se generează devizul..."):
            nr_oferta = nr_devize + 1
            cod_oferta = f"OF-2025-{nr_oferta:04d}_{nume_client.replace(' ', '')}"
            prompt_final = prompt
            if foloseste_gpt:
                prompt_final = f"Generează un deviz complet pentru un {tip_mobilier} cu dimensiunile {inaltime}x{latime}x{adancime} mm. {prompt}"
            rezultat = genereaza_deviz_AI(prompt_final)

            st.success("✅ Deviz generat cu succes!")
            st.markdown(f"**Număr ofertă:** `{cod_oferta}`")
            st.text_area("Deviz:", rezultat, height=300)

            meta = {
                "cod_oferta": cod_oferta,
                "nume_client": nume_client,
                "telefon": telefon_client,
                "dimensiuni": [inaltime, latime, adancime],
                "tip": tip_mobilier,
                "prompt": prompt,
                "valoare_total": 0,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            # Structură minimală pentru export
            content = [{
                "Produs": tip_mobilier,
                "Cod": "AI-001",
                "UM": "buc",
                "Cantitate": 1,
                "Pret": 1000.00  # exemplu fix, înlocuibil cu analiză reală
            }]
            meta["valoare_total"] = 1000.00

            save_offer(meta, content)

            if st.button("📤 Exportă PDF și Excel"):
                st.success("Fișierele au fost exportate în folderul output/")

# 📜 Istoric oferte
if istoric_path.exists():
    st.subheader("📂 Oferte recente")
    files = sorted(list(output_dir.glob("OF-*.json")), reverse=True)[:10]
    for f in files:
        with open(f, "r") as json_f:
            data = json.load(json_f)
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"🔖 `{data['cod_oferta']}` – {data['nume_client']} | {data['dimensiuni']} | {data['data']} | {data['valoare_total']} lei")
        with col2:
            st.image("assets/placeholder.png", width=40)
