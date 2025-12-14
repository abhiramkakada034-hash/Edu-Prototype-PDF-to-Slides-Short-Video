# src/pdf_extractor.py
from dotenv import load_dotenv
import pdfplumber
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")


def extract_key_sections(pdf_path, num_sections=8):
    """
    Extract text from PDF and use LLM to identify top N key sections.
    """
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Use Groq via LangChain to extract key points
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["text", "num"],
        template="Extract and rank the top {num} key points or sections from this document text. Output as a numbered list: {text}"
    )
    chain = prompt | llm  # Use LCEL instead of LLMChain

    result = chain.invoke({"text": full_text[:20000], "num": num_sections}).content  # Get content from AIMessage

    # Parse result into list of sections
    sections = []
    for line in result.split('\n'):
        if line.strip() and line[0].isdigit():
            sections.append({'full_text': line.strip()})

    return sections[:num_sections]  # Ensure 6-10