import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient

def verify_claims(claims):
    """Verify each claim using web search + LangChain"""
    results = []
    
    try:
        # Initialize LangChain Groq LLM
        llm = ChatGroq(
            api_key=st.secrets["GROQ_API_KEY"],
            model="llama-3.3-70b-versatile",  # ← CHANGED THIS
            temperature=0
        )
        
        # Initialize Tavily for web search
        tavily_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        
        # Create verification prompt template
        verification_prompt = PromptTemplate(
            input_variables=["claim", "search_results"],
            template="""You are a professional fact-checker. Analyze this claim against real-time web search results.

CLAIM TO VERIFY:
{claim}

SEARCH RESULTS FROM THE WEB:
{search_results}

Your task:
1. Determine if the claim is VERIFIED, INACCURATE, or FALSE
2. Provide clear reasoning based on the search results
3. If inaccurate/false, provide the correct information with specific details

Respond in this format:
STATUS: [VERIFIED/INACCURATE/FALSE]
REASONING: [Your detailed analysis]
CORRECT_INFO: [If applicable, the accurate information with numbers/dates]

Be precise and cite specific facts from the search results."""
        )
        
        # Create chain
        chain = verification_prompt | llm | StrOutputParser()
        
        # Verify each claim
        for i, claim in enumerate(claims, 1):
            st.write(f"Verifying claim {i}/{len(claims)}...")
            
            # Search the web for information
            search_results = tavily_client.search(
                query=claim,
                max_results=5,
                search_depth="advanced"
            )
            
            # Prepare context from search results
            context = "\n\n".join([
                f"Source {idx+1}: {result['url']}\nContent: {result['content']}" 
                for idx, result in enumerate(search_results.get('results', []))
            ])
            
            if not context:
                context = "No search results found for this claim."
            
            # Run verification chain
            verification = chain.invoke({
                "claim": claim,
                "search_results": context
            })
            
            # Parse the status
            status = "UNKNOWN"
            if "STATUS: VERIFIED" in verification:
                status = "VERIFIED"
            elif "STATUS: INACCURATE" in verification:
                status = "INACCURATE"
            elif "STATUS: FALSE" in verification:
                status = "FALSE"
            
            # Extract reasoning and correct info
            lines = verification.split('\n')
            reasoning = ""
            correct_info = ""
            
            for line in lines:
                if line.startswith('REASONING:'):
                    reasoning = line.replace('REASONING:', '').strip()
                elif line.startswith('CORRECT_INFO:'):
                    correct_info = line.replace('CORRECT_INFO:', '').strip()
            
            results.append({
                "claim": claim,
                "status": status,
                "reasoning": reasoning,
                "correct_info": correct_info,
                "full_analysis": verification,
                "sources": [r['url'] for r in search_results.get('results', [])]
            })
        
        return results
    
    except Exception as e:
        st.error(f"Error verifying claims: {str(e)}")
        return []
