import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from groq import Groq

def extract_claims(text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = f"""Extract all specific factual claims from this text. 
    Focus on: statistics, dates, financial figures, technical specifications.
    
    Text: {text}
    
    Return as a numbered list."""
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
        temperature=0
    )
    
    return response.choices[0].message.content


