from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain_classic.output_parsers.fix import OutputFixingParser  # New import for fixing invalid JSON

def summarize_sections(sections):
    """
    For each section, generate slide title, bullets, and notes.
    """
    response_schemas = [
        ResponseSchema(name="title", description="Slide headline, concise and engaging (6-20 words)"),
        ResponseSchema(name="bullets", description="Exactly 1-2 short supporting bullet points as a list of strings"),
        ResponseSchema(name="notes", description="One clear sentence for narration/TTS")
    ]
    base_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    output_parser = OutputFixingParser.from_llm(parser=base_parser, llm=ChatGroq(model="llama3-8b-8192"))  # Wrap with fixer
    format_instructions = base_parser.get_format_instructions()

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1)  # Or llama3-70b-8192 for better JSON adherence

    prompt = PromptTemplate(
        template="""You are an expert slide creator. Summarize the section below into slide content.
Output ONLY a valid JSON object with no extra text, explanations, or markdown. Ensure proper JSON syntax with commas between keys.

{format_instructions}

Section text:
{section}""",
        input_variables=["section"],
        partial_variables={"format_instructions": format_instructions}
    )

    chain = prompt | llm | output_parser  # Use the fixing parser in the chain

    slides_data = []
    for section in sections:
        try:
            parsed = chain.invoke({"section": section['full_text']})
            # Normalize bullets
            if 'bullets' in parsed and isinstance(parsed['bullets'], str):
                parsed['bullets'] = [b.strip() for b in parsed['bullets'].split('\n') if b.strip()][:2]
            elif isinstance(parsed.get('bullets'), list):
                parsed['bullets'] = parsed['bullets'][:2]
            else:
                parsed['bullets'] = []
            slides_data.append(parsed)
        except Exception as e:
            print(f"Parsing failed even with fixer: {e}. Using fallback slide.")
            slides_data.append({
                "title": "Important Concept",
                "bullets": ["Key point from section", "Supporting detail"],
                "notes": "This slide covers a main idea from the document."
            })

    return slides_data