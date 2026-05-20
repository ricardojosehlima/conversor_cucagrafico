from openai import OpenAI
import streamlit as st

SYSTEM_PROMPT = """
You convert text from an alternative Portuguese orthography into standard Portuguese orthography.

Rules:
- Preserve meaning.
- Preserve punctuation and paragraph breaks.
- Return only the converted text.
- Do not explain.
- Do not add notes.
- Do not put quotation marks around the output.
- If the input is already close to standard orthography, normalize it into standard orthography.
""".strip()


def convert_alternative_to_standard(texto: str) -> str:
    if not texto or not texto.strip():
        return ""

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    response = client.responses.create(
        model="gpt-5.4",
        reasoning={"effort": "none"},
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": SYSTEM_PROMPT}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": texto}
                ],
            },
        ],
    )

    return response.output_text.strip()