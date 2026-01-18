import streamlit as st
from services.pdf_loader import load_pdf_text
from services.claim_extractor import extract_claims
from services.verifier import verify_claims

st.set_page_config(page_title="Fact Checker", layout="wide")

st.title("📄 AI Fact-Checking Web App")
st.write("Upload a PDF. The app will extract factual claims and verify them against live web data.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading PDF..."):
        text = load_pdf_text(uploaded_file)

    with st.spinner("Extracting claims..."):
        claims = extract_claims(text)

    if not claims:
        st.warning("No factual claims detected.")
    else:
        with st.spinner("Verifying claims using live web search..."):
            results = verify_claims(claims)

        st.subheader("Fact-Check Results")

        for r in results:
            st.markdown(f"### 🔍 Claim")
            st.write(r["claim"])

            status = r["status"]
            if status == "Verified":
                st.success(f"✅ {status}")
            elif status == "Inaccurate":
                st.warning(f"⚠️ {status}")
            else:
                st.error(f"❌ {status}")

            st.write("**Evidence:**")
            st.write(r["evidence"])
            st.divider()
