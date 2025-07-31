import streamlit as st
from ai_generator import genereaza_deviz_AI
from deviz_exporter import export_excel, export_pdf
from dotenv import load_dotenv
import os
from PIL import Image
import json
from datetime import datetime
from pathlib import Path

load_dotenv()
st.set_page_config(page_title="Kuziini | Generator Devize", layout="wide")

# Logo
if Path("Kuziini_logo_negru.png").exists():
    st.image("Kuziini_logo_negru.png", width=250)

st.title("Kuziini | Configurator AI Devize Mobilier")

# Date client
col1, col2 = st.columns(2)
with col1:
    nume_client = st.text_input("Nume client")
with col2:
    telefon_client = st.text_input("Telefon client")

# Imagine
poza = st.file_uploader("Încarcă o schiță (opțional)", type=["jpg", "png"])

# Dimensiuni
st.subheader("Dimensiuni (mm)")
col1, col2, col3 = st.columns(3)
with col1:
    inaltime = st.number_input("Înălțime", min_value=0)
with col2:
    latime = st.number_input("Lățime", min_value=0)
with col3:
    adancime = st.number_input("Adâncime", min_value=0)

# Face parte dintr-un ansamblu?
st.subheader("Face parte dintr-un ansamblu?")
este_ansamblu = st.checkbox("✔️ Da, acest corp face parte dintr-un ansamblu")
nume_ansamblu = ""
if este_ansamblu:
    nume_ansamblu = st.text_input("Nume proiect / ansamblu", value="")

# Tip mobilier
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

# Descriere prompt
st.subheader("Descriere suplimentară")
prompt_initial = st.text_area("Scrie detalii despre mobilier, decor, funcționalitate etc.")

foloseste_gpt = st.checkbox("Folosește GPT pentru rescriere prompt", value=True)

# Devize salvate
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
istoric_path = output_dir / "istoric.json"

# Buton generare
if st.button("Generează ofertă"):
    with st.spinner("Se generează devizul..."):
        prompt_final = prompt_initial
        if foloseste_gpt:
            prompt_final = f"Generează un deviz complet pentru un {tip_mobilier} cu dimensiunile {inaltime} x {latime} x {adancime} mm. Detalii: {prompt_initial}"

        rezultat = genereaza_deviz_AI(prompt_final)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cod_deviz = f"OF-{timestamp}_{nume_client.replace(' ', '_')}"
        output_json = output_dir / f"{cod_deviz}.json"

        info = {
            "client": nume_client,
            "telefon": telefon_client,
            "dimensiuni": [inaltime, latime, adancime],
            "tip": tip_mobilier,
            "prompt": prompt_initial,
            "rezultat": rezultat,
            "ansamblu": nume_ansamblu if este_ansamblu else None,
            "timestamp": timestamp
        }

        with open(output_json, "w") as f:
            json.dump(info, f, indent=2)

        st.success("✅ Devizul a fost generat!")
        st.text_area("Deviz generat:", rezultat, height=300)

# Istoric
if istoric_path.exists():
    st.subheader("📂 Istoric devize generate")
    with open(istoric_path, "r") as f:
        istoric = json.load(f)
    for idx, item in enumerate(reversed(istoric[-5:])):
        st.markdown(f"**{item['client']}** | {item['tip']} | {item['dimensiuni']} | Prompt: _{item['prompt'][:40]}..._")