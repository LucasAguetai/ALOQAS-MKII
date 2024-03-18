import requests
import streamlit as st
import json


model = st.selectbox('which model would you like to use',
                    ('MobileBERT', 'BERT', 'DeBERTa-v2'))


userInput = st.text_input(f"write to the {model}")

contextSelect = st.radio("Pick a context mode:", ["File", "Text"])
if contextSelect == "File":
    userContext = st.file_uploader("Pick a file for the context", accept_multiple_files=True)
    context = "/uploadfile"
else:
    userContext = st.text_input("write the context")
    context = "/contextText"

siteUrl = "http://127.0.0.1:8000"

if st.button("Envoyer la requête"):
    params = {'texte': userInput, "model": model}
    if userContext is not None:
        if contextSelect == "File":
            files = {"file": (userContext.name, userContext, userContext.type)}
            response = requests.post(
                siteUrl+context, params=params, files=files)
        else:
            params["context"] = userContext
            print(params)
            response = requests.post(siteUrl+context, params=params)
    else:
        response = requests.post(siteUrl+'/withoutFile', params=params)

    st.write("Statut de la requête:", response.status_code)
    st.write("Réponse du serveur:", response.text)
