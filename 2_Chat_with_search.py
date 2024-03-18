import streamlit as st
import requests
import streamlit as st

siteUrl = "http://127.0.0.1:8000"

userContext = None
context = None

with st.sidebar:
    model = st.selectbox('which model would you like to use',
                         ('MobileBERT', 'BERT', 'DeBERTa-v2'))
    contextSelect = st.radio("Pick a context mode:", ["File", "Text"])
    if contextSelect == "File":
        userContext = st.file_uploader("Pick a file for the context", accept_multiple_files=True)
        context = "/uploadfile"
    else:
        userContext = st.text_input("write the context")
        context = "/contextText"

st.title("ALOQAS")

"""
bla bla bla
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm ALOQAS. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Write to ALOQAS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    params = {'texte': prompt, "model": model}
    if userContext is not None:
        if contextSelect == "File" and userContext:
            # Préparation de la liste des fichiers pour l'envoi
            files = [("file", (file.name, file, file.type)) for file in userContext]
            response = requests.post(siteUrl + context, params=params, files=files)
        else:
            params["context"] = userContext
            response = requests.post(siteUrl + context, params=params)
    else:
        response = requests.post(siteUrl + '/withoutFile', params=params)

    st.write("Statut de la requête:", response.status_code)
    st.write("Réponse du serveur:", response.text)
