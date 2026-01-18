import streamlit as st
from groq import Groq

def extract_claims(text):
    """Extract factual claims from text using Groq"""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""You are a fact-checking assistant. Extract ALL specific factual claims from the following text.
        
Focus on:
- Statistics and numbers
- Dates and timeframes
- Financial figures (prices, revenue, market cap, etc.)
- Technical specifications
- Quotes attributed to people
- Historical events

Format each claim as a separate line starting with "CLAIM: "

Text to analyze:
{text}

Extract the claims:"""
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0,
            max_tokens=2000
        )
        
        claims_text = response.choices[0].message.content
        
        # Parse claims into a list
        claims = []
        for line in claims_text.split('\n'):
            if line.strip().startswith('CLAIM:'):
                claim = line.replace('CLAIM:', '').strip()
                if claim:
                    claims.append(claim)
        
        return claims
    
    except Exception as e:
        st.error(f"Error extracting claims: {str(e)}")
        return []
