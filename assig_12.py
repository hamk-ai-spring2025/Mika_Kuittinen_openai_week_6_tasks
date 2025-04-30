import streamlit as st
import openai
import os

# Käytetään ympäristömuuttujaa API-avaimen lukemiseen
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Multi-LLM Chat", layout="centered")
st.title("💬 Multi-LLM Chat App")

# Mallin valinta sivupalkissa
model_choice = st.sidebar.selectbox("Valitse kielimalli", ["GPT-3.5", "Mock-Falcon"])

# Käyttäjän syöte
user_input = st.text_input("Sinä:", placeholder="Kirjoita kysymys tai viesti tähän")

# Funktio: kysy GPT-3.5:lta
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Virhe GPT-3.5-kyselyssä: {e}"

# Mockattu Falcon-malli (ei oikea yhteys)
def ask_falcon(prompt):
    return f"🦅 Falcon 7B (mock) vastaa: '{prompt}'"

# Näytetään vastaus, jos käyttäjä kirjoitti jotain
if user_input:
    if model_choice == "GPT-3.5":
        reply = ask_openai(user_input)
    else:
        reply = ask_falcon(user_input)

    st.markdown("**LLM:n vastaus:**")
    st.info(reply)