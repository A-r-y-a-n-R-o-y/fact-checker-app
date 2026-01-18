import os
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatGroq

def extract_claims(text: str):
    # Initialize the model
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0
    )

    # Define the prompt
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
Extract factual, checkable claims from the following text.
Only return bullet points containing statistics, dates, financial figures,
or concrete verifiable assertions.

Text:
{text}
"""
    )

    # Generate response
    response = llm(prompt.format(text=text))  # Use __call__ instead of invoke

    # Extract claims
    claims = response.content.split("\n")  # Check response structure if needed
    claims = [c.strip("- ").strip() for c in claims if c.strip()]

    return claims
