import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_answers(contexts, queries):

    payload = []

    for i, (query, retrieved_chunks) in enumerate(
        zip(queries, contexts), start=1
    ):
        payload.append(
            {
                "query_id": i,
                "question": query,
                "context": retrieved_chunks
            }
        )

    prompt = f"""
        Answer each query independently.

        For every query:
        - Use ONLY its associated context.
        - Do NOT use information from other queries.
        - If the answer is not present, return:
        "I cannot find the answer in the provided documents."

        Input:

        {json.dumps(payload, indent=2)}

        Return ONLY valid JSON:

        {{
            "answers": [
                {{
                    "query_id": 1,
                    "answer": "..."
                }}
            ]
        }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="""
                Use only the context attached to each query to answer them.
                Never use information from another query's context.
                Return only valid JSON.
            """,
            temperature=0.0,
        ),
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]      # remove ```json

    if text.endswith("```"):
        text = text[:-3]     # remove closing ```

    text = text.strip()

    result = json.loads(text)
    return result

