from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query):
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )
    return response["results"]
