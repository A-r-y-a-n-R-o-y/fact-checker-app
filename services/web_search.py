import streamlit as st
from tavily import TavilyClient

def search_claim(claim):
    # Access Tavily API key from secrets
    tavily_api_key = st.secrets["TAVILY_API_KEY"]
    
    # Initialize Tavily client
    client = TavilyClient(api_key=tavily_api_key)
    
    # Search for the claim
    response = client.search(claim, max_results=3)
    
    return response
