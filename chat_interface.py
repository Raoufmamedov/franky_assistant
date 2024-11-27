import streamlit as st
import requests

st.set_page_config(page_title="Knowledge Assistant", layout="wide")

# API endpoints
UPLOAD_ENDPOINT = "http://127.0.0.1:8000/upload/"
TRAIN_ENDPOINT = "http://127.0.0.1:8000/train/"
QUERY_ENDPOINT = "http://127.0.0.1:8000/query/"

st.title("Knowledge Assistant")

# Upload section
st.sidebar.header("Upload Files")
uploaded_file = st.sidebar.file_uploader("Upload your files", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
    response = requests.post(UPLOAD_ENDPOINT, files=files)
    st.sidebar.success(response.json()["info"])

if st.sidebar.button("Train Knowledge Base"):
    response = requests.post(TRAIN_ENDPOINT)
    st.sidebar.success(response.json()["info"])

# Query section
st.header("Ask Your Assistant")
query = st.text_input("Enter your question:")

if st.button("Search"):
    if query.strip():
        response = requests.post(QUERY_ENDPOINT, json={"query": query})
        results = response.json().get("results", [])
        for i, result in enumerate(results):
            st.write(f"**Result {i + 1}:** {result}")
    else:
        st.error("Please enter a valid query.")
