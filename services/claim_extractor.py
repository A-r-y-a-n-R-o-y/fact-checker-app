import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def extract_claims(text):
    """Extract factual claims using LangChain + Groq"""
    try:
        # Initialize Groq LLM through LangChain
        llm = ChatGroq(
            api_key=st.secrets["GROQ_API_KEY"],
            model="mixtral-8x7b-32768",
            temperature=0
        )
        
        # Create prompt template
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""You are a fact-checking assistant. Extract ALL specific factual claims from the following text.

Focus on:
- Statistics and numbers (e.g., "GDP grew by 5%", "Stock price is $150")
- Dates and timeframes (e.g., "In 2023...", "Last quarter...")
- Financial figures (revenue, market cap, prices, etc.)
- Technical specifications (speeds, sizes, capacities)
- Quotes attributed to specific people
- Historical events and facts

Format: Return each claim on a new line starting with "CLAIM: "

Text to analyze:
{text}

Extract all verifiable claims:"""
        )
        
        # Create chain
        chain = prompt | llm | StrOutputParser()
        
        # Run the chain
        result = chain.invoke({"text": text})
        
        # Parse claims into a list
        claims = []
        for line in result.split('\n'):
            line = line.strip()
            if line.startswith('CLAIM:'):
                claim = line.replace('CLAIM:', '').strip()
                if claim:
                    claims.append(claim)
        
        return claims
    
    except Exception as e:
        st.error(f"Error extracting claims: {str(e)}")
        return []
