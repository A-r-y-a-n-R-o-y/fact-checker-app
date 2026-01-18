import streamlit as st
from services.pdf_loader import load_pdf_text
from services.claim_extractor import extract_claims
from services.verifier import verify_claims

st.set_page_config(page_title="Fact Checker", layout="wide", page_icon="🔍")

st.title("🔍 Fact-Checking Web App")
st.markdown("**Powered by LangChain + Groq + Tavily**")
st.write("Upload a PDF to automatically extract and verify factual claims against live web data")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This app uses:")
    st.write("- **LangChain** for LLM orchestration")
    st.write("- **Groq (Mixtral)** for AI analysis")
    st.write("- **Tavily** for web search")
    st.write("- **PyPDF2** for PDF parsing")

# File uploader
uploaded_file = st.file_uploader("📄 Upload PDF Document", type=['pdf'])

if uploaded_file:
    with st.spinner("📖 Extracting text from PDF..."):
        text = load_pdf_text(uploaded_file)
    
    if text:
        st.success(f"✅ Extracted {len(text):,} characters from PDF")
        
        with st.expander("📝 View extracted text (preview)"):
            st.text(text[:2000] + "..." if len(text) > 2000 else text)
        
        if st.button("🔍 Extract and Verify Claims", type="primary", use_container_width=True):
            
            # Step 1: Extract claims
            with st.spinner("🤖 Extracting claims using LangChain + Groq..."):
                claims = extract_claims(text)
            
            if not claims:
                st.warning("⚠️ No claims found in the document.")
            else:
                st.success(f"✅ Found **{len(claims)}** claims to verify")
                
                with st.expander("📋 View extracted claims"):
                    for i, claim in enumerate(claims, 1):
                        st.write(f"{i}. {claim}")
                
                # Step 2: Verify claims
                st.write("---")
                st.subheader("🔎 Verification Results")
                
                with st.spinner("🌐 Verifying claims against live web data..."):
                    results = verify_claims(claims)
                
                # Display results
                verified_count = sum(1 for r in results if r['status'] == 'VERIFIED')
                inaccurate_count = sum(1 for r in results if r['status'] == 'INACCURATE')
                false_count = sum(1 for r in results if r['status'] == 'FALSE')
                
                col1, col2, col3 = st.columns(3)
                col1.metric("✅ Verified", verified_count)
                col2.metric("⚠️ Inaccurate", inaccurate_count)
                col3.metric("❌ False", false_count)
                
                st.write("---")
                
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
                    
                    with st.expander(f"{icon} **Claim {i}:** {result['claim'][:100]}{'...' if len(result['claim']) > 100 else ''}"):
                        st.markdown(f"**Status:** :{color}[**{status}**]")
                        
                        st.write("**📊 Reasoning:**")
                        st.write(result['reasoning'] if result['reasoning'] else result['full_analysis'])
                        
                        if result['correct_info']:
                            st.write("**✏️ Correct Information:**")
                            st.info(result['correct_info'])
                        
                        st.write("**🔗 Sources:**")
                        for source in result['sources'][:3]:
                            st.write(f"- {source}")
else:
    st.info("👆 Please upload a PDF document to get started")
