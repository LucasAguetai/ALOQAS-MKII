import streamlit as st
import requests
import json

# Define initial configurations and variables
siteUrl = "https://aloqas-aloqas-qa-fastapi.hf.space"
response = None
userContext = None
context = None
error = 0
limit = 9000
model = None


def on_change_write_name_of_model():
    selected_model = st.session_state['model']
    st.session_state.messages.append({"role": "assistant", "content": f"Switched to {selected_model} model."})

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    # Define a selectbox for model selection
    model = st.selectbox('Which model would you like to use?',
                         ('SqueezeBERT', 'BERT', 'DeBERTa'), index=1,
                         help="SqueezeBERT is faster but less accurate, BERT is balanced, and DeBERTa is slower but more accurate.",
                         on_change=on_change_write_name_of_model, key='model')
    # Define a radio button group for context mode selection
    contextSelect = st.radio("Pick a context mode:", ["Text", "File"], index=0, help="Choose between text or file context.")
    if contextSelect == "File":
        userContext = st.file_uploader("Pick a file for the context", accept_multiple_files=True, help="Upload files of types: txt, json, docx, pdf, csv for context.", type=['txt', 'json', 'docx', 'pdf', 'csv'])
        context = "/uploadfile/"
    else:
        userContext = st.text_area("Write the context", max_chars=limit, help="Insert the context text here.")
        context = "/contextText/"

# Main page title
st.title("ALOQAS")

# Dynamic welcome message based on model and context selection
if model and contextSelect:
    if model == 'DeBERTa':
        model_info = "Using the DeBERTa model for the most accurate answers, although it may be slower."
    elif model == 'SqueezeBERT':
        model_info = "Using the SqueezeBERT model for faster but less precise answers."
    else:
        model_info = "Using the BERT model as a balance between speed and accuracy."

    if contextSelect == "File":
        context_info = "Upload files of types: txt, json, docx, pdf, csv for context."
    else:
        context_info = f"Insert text context up to {limit} characters."

    st.subheader("Welcome to ALOQAS AI")
    st.write(f"{model_info} {context_info}")
    st.write("")
    st.write("")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm ALOQAS. How can I help you?"}
    ]

if prompt := st.chat_input(placeholder="Write to ALOQAS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    params = {'question': prompt, "model": model.lower()}

    if userContext != '' and len(userContext) <= limit:
        if contextSelect == "File" and userContext:
            files = [("files", (file.name, file, file.type)) for file in userContext]
            response = requests.post(siteUrl + context, data=params, files=files)
            st.session_state.messages.append({"role": "assistant", "content": json.loads(response.text).get("answer", "Sorry, I couldn't find an answer for your question.")})
        else:
            params["context"] = userContext
            response = requests.post(siteUrl + context, json=params)
            st.session_state.messages.append({"role": "assistant", "content": json.loads(response.text).get("answer", "Sorry, I couldn't find an answer for your question.")})

    if response is None:
        error = 3
    if userContext != '' and len(userContext) <= limit and response is not None:
        with st.sidebar:
            st.markdown(f"<div style='color: white; background-color: #0F1116 ; padding: 10px; border-radius: 5px;'><h2 style='color: white;'>Statistics on the last answer</h2><p>Time: {json.loads(str(round(response.elapsed.total_seconds(), 2)))}s</p><p>Score: {round(json.loads(response.text).get('score', 0), 2)}</p><p>Start: {json.loads(response.text).get('start', 0)}</p><p>End: {json.loads(response.text).get('end', 0)}</p></div>", unsafe_allow_html=True)

    elif userContext == '' :
        error = 1
    elif len(userContext) > limit:
        error = 2
    else:
        error = 3

for msg in st.session_state.messages:
    st.chat_message(msg.get("role", "assistant")).write(msg.get("content", "Hi, I'm ALOQAS. How can I help you?"))


if error == 1:
    message_rouge = "⚠️ Please provide a context via the menu on your left."
    st.markdown(f'<div style="color: white; background-color: #ff4444; padding: 10px; border-radius: 5px;">{message_rouge}</div>', unsafe_allow_html=True)
    error = 0
elif error == 2:
    message_rouge = f"⚠️ The message you submitted was too long, please reload the conversation and submit something shorter than {limit} characters."
    st.markdown(f'<div style="color: white; background-color: #ff4444; padding: 10px; border-radius: 5px;">{message_rouge}</div>', unsafe_allow_html=True)
    error = 0
elif error == 3:
    message_rouge = f"⚠️ An error occurred, please try again."
    st.markdown(f'<div style="color: white; background-color: #ff4444; padding: 10px; border-radius: 5px;">{message_rouge}</div>', unsafe_allow_html=True)
    error = 0
else:
    st.write("")
