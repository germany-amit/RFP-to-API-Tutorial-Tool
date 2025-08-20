import streamlit as st
import json
import re

st.set_page_config(page_title="API Advisor MVP", layout="wide")

st.title("📑 API Advisor from RFP")

# ---- File Upload ----
uploaded = st.file_uploader("Upload RFP (PDF/TXT)", type=["txt", "pdf"])

text = ""
if uploaded:
    if uploaded.type == "application/pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded)
            text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except Exception as e:
            text = f"Error reading PDF: {e}"
    else:
        text = uploaded.read().decode("utf-8")

st.text_area("📄 Extracted RFP Text", value=text, height=200)

# ---- What is API ----
st.subheader("ℹ️ What is an API?")
st.write(
    "An API (Application Programming Interface) allows two software systems to communicate. "
    "It defines **endpoints, methods, and data formats**. Common types: REST (JSON over HTTP), GraphQL, gRPC."
)

# ---- Requirement Interpretation ----
st.subheader("🔍 Requirement Interpretation")
keywords = []
if text:
    keywords = re.findall(r"\b(?:secure|auth|json|xml|real-time|scalable|report|user|data)\b", text.lower())
    keywords = list(set(keywords))
st.write("**Detected keywords:**", ", ".join(keywords) if keywords else "None found")

# ---- Suggested API Type ----
st.subheader("📌 Suggested API Type")
api_type = "REST API (standard JSON over HTTP)"
if "real-time" in keywords:
    api_type = "gRPC (real-time, high-performance)"
elif "report" in keywords or "flexible" in keywords:
    api_type = "GraphQL API (flexible queries over structured data)"
st.success(api_type)

# ---- Data Modeling (Simple JSON Schema) ----
st.subheader("🗂 Example Data Model (JSON Schema)")
entities = [w for w in ["user", "order", "product", "report"] if w in text.lower()]
schema = {
    "type": "object",
    "properties": {e: {"type": "string"} for e in entities} or {"sample_field": {"type": "string"}},
}
st.json(schema)

# ---- Security Boilerplate ----
st.subheader("🔒 Security Boilerplate Snippet (FastAPI)")
code = """from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/secure-data/")
def read_secure(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected endpoint"}
"""
st.code(code, language="python")

# ---- Download Spec File ----
st.subheader("📤 Export Draft API Spec")
spec = {
    "api_type": api_type,
    "keywords": keywords,
    "schema": schema,
}
st.download_button("Download OpenAPI Draft (JSON)", data=json.dumps(spec, indent=2),
                   file_name="api_spec.json", mime="application/json")
