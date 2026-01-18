import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

def extract_claims(text):
    # Access API key from Streamlit secrets
    groq_api_key = st.secrets["GROQ_API_KEY"]
    
    # Initialize Groq LLM
    llm = ChatGroq(
        temperature=0,
        groq_api_key=groq_api_key,
        model_name="mixtral-8x7b-32768"  # or "llama2-70b-4096"
    )
    
    #claim extraction logic here
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Extract all factual claims from this text: {text}"
    )
    
