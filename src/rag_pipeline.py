import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def answer_with_context(query, context):
    # 1. Combine all retrieved text chunks into one organized string
    context_block=""

    for retrieved_chunks in context:
        context_block += "\n---\n".join(retrieved_chunks)
        context_block += "content for repsective query.\n" 

    # 2. Construct the structured prompt payload
    prompt = f"""
    CONTEXTS FROM DOCUMENTS:
    {context_block}
    
    USER QUESTIONS:
    {query}
    """
    
    # 3. Configure strict system rules to prevent hallucinations
    system_rules = (
        "You are a precise factual assistant. Answer the user question using ONLY the provided "
        "Context From Documents. If the context does not contain the answer, say "
        "'I cannot find the answer in the provided documents.' Do not make things up."
    )
    
    # 4. Execute the call
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt, 
        config=types.GenerateContentConfig(
            system_instruction=system_rules,
            temperature=0.0,  # CRITICAL: Keep at 0.0 for strict factual accuracy
            top_p=0.95,
        ),
    )
    return response.text


