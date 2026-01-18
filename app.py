import streamlit as st
from services.pdf_loader import load_pdf_text
from services.claim_extractor import extract_claims
from services.verifier import verify_claims

st.set_page_config(page_title="Fact Checker", layout="wide")

st.title("🔍 Fact-Checking Web App")
st.write("Upload a PDF to verify factual claims against live web data")

# File uploader
uploaded_file = st.file_uploader("Upload PDF Document", type=['pdf'])

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        text = load_pdf_text(uploaded_file)
    
    if text:
        st.success(f"✅ Extracted {len(text)} characters from PDF")
        
        with st.expander("View extracted text"):
            st.text(text[:1000] + "..." if len(text) > 1000 else text)
        
        if st.button("🔍 Extract and Verify Claims", type="primary"):
            with st.spinner("Extracting claims..."):
                claims = extract_claims(text)
            
            st.write(f"### Found {len(claims)} claims to verify")
            
            with st.spinner("Verifying claims against web data..."):
                results = verify_claims(claims)
            
            # Display results
            st.write("### Verification Results")
            
            for i, result in enumerate(results, 1):
                status = result['status']
                
                if status == "VERIFIED":
                    icon = "✅"
                    color = "green"
                elif status == "INACCURATE":
                    icon = "⚠️"
                    color = "orange"
                else:
                    icon = "❌"
                    color = "red"
                
                with st.expander(f"{icon} Claim {i}: {result['claim'][:100]}..."):
                    st.markdown(f"**Status:** :{color}[{status}]")
                    st.write("**Analysis:**")
                    st.write(result['explanation'])
                    st.write("**Sources:**")
                    for source in result['sources']:
                        st.write(f"- {source}")
