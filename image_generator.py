import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

# Hugging Face API-tunnus haetaan ympäristömuuttujasta
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Kuvan generointifunktio
def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    try:
        content_type = response.headers.get("content-type")
        if "image" not in content_type:
            return None, response.json()
        return response.content, None
    except:
        return None, {"error": "Tuntematon virhe tai yhteysongelma."}

# Streamlit UI
st.set_page_config(page_title="AI Image Generator", layout="centered")
st.title("🎨 AI Image Generator")

prompt = st.text_input("Prompt (haluttu sisältö)", "A futuristic city at night")
aspect_ratio = st.selectbox("Kuvasuhde (ei vaikuta malliin, visuaalinen valinta)", ["1:1", "16:9", "9:16"])

if st.button("Generoi kuva"):
    with st.spinner("Luodaan kuvaa..."):
        image_bytes, error = query(prompt)

    if error:
        st.error(f"Kuvan generointi epäonnistui: {error}")
    else:
        try:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Generoitu kuva", use_column_width=True)

            image.save("generated_image.png")
            with open("generated_image.png", "rb") as file:
                st.download_button("Lataa kuva", file, "generated_image.png", "image/png")
        except Exception as e:
            st.error(f"Kuvan käsittely epäonnistui: {e}")