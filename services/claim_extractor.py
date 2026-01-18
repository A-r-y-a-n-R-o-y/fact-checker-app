from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

def extract_claims(text):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
Extract factual, checkable claims from the following text.
Only return bullet points with statistics, dates, financial figures, or concrete assertions.

Text:
{text}
"""
    )

    response = llm.invoke(prompt.format(text=text))
    claims = response.content.split("\n")
    claims = [c.strip("- ").strip() for c in claims if c.strip()]
    return claims
