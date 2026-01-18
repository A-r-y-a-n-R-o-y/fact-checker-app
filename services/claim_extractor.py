import os
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatGroq

def extract_claims(text: str):
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0
    )

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

    response = llm.invoke(prompt.format(text=text))

    claims = response.content.split("\n")
    claims = [c.strip("- ").strip() for c in claims if c.strip()]

    return claims
