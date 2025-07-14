import streamlit as st
import requests

st.set_page_config(page_title="QA ChatBot", layout="wide")
st.title("QA ChatBot")
st.subheader("Upload a PDF file to start...")


uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
if uploaded_file and "uploaded" not in st.session_state:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading and processing..."):
        res = requests.post("http://127.0.0.1:8000/ingest", files=files)

    if res.status_code == 200:
        st.session_state.uploaded = True
        st.success(res.json()["message"])
    else:
        st.error(f"Error: {res.json().get('error', 'Unknown error')}")



st.subheader("Ask a question based on the uploaded PDF")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your question")

if user_input:
    with st.spinner("Generating answer"):
        res = requests.post("http://127.0.0.1:8000/query", json={"question": user_input})

    if res.status_code == 200:
        answer = res.json()["answer"]
        st.markdown(f"Answer:{answer}")
        st.session_state.chat_history.append((user_input, answer))
    else:
        st.error(f"Error: {res.json().get('error', 'Query failed')}")


if st.session_state.chat_history:
    st.subheader("Chat History")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"Qns: {q}")
        st.markdown(f"Ans: {a}")
