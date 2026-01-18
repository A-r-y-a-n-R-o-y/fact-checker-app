import PyPDF2
import streamlit as st

def load_pdf_text(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text
    
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""
