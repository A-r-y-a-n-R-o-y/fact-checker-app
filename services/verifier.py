import streamlit as st
from groq import Groq
from tavily import TavilyClient

def verify_claims(claims):
    """Verify each claim using web search"""
    results = []
    
    try:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        tavily_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        
        for claim in claims:
            # Search the web for information about the claim
            search_results = tavily_client.search(
                query=claim,
                max_results=3,
                search_depth="advanced"
            )
            
            # Prepare context from search results
            context = "\n\n".join([
                f"Source: {result['url']}\n{result['content']}" 
                for result in search_results.get('results', [])
            ])
            
            # Ask Groq to verify the claim
            verification_prompt = f"""You are a fact-checker. Based on the search results below, verify this claim:

CLAIM: {claim}

SEARCH RESULTS:
{context}

Analyze the claim and respond with:
1. STATUS: Either "VERIFIED", "INACCURATE", or "FALSE"
2. EXPLANATION: Brief explanation of why
3. CORRECT_INFO: If inaccurate or false, provide the correct information

Be precise and cite specific details from the search results."""
            
            response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": verification_prompt}],
                model="mixtral-8x7b-32768",
                temperature=0,
                max_tokens=500
            )
            
            verification = response.choices[0].message.content
            
            # Parse the status
            status = "UNKNOWN"
            if "VERIFIED" in verification.upper():
                status = "VERIFIED"
            elif "INACCURATE" in verification.upper():
                status = "INACCURATE"
            elif "FALSE" in verification.upper():
                status = "FALSE"
            
            results.append({
                "claim": claim,
                "status": status,
                "explanation": verification,
                "sources": [r['url'] for r in search_results.get('results', [])]
            })
        
        return results
    
    except Exception as e:
        st.error(f"Error verifying claims: {str(e)}")
        return []
