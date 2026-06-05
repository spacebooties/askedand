import os
import ollama

MODEL = os.getenv("OLLAMA_MODEL", "gemma3")


def run(topic):

    prompt = f"""
Generate ONE thoughtful political or philosophical question.

Topic:
{topic}

Rules:
- Return only the question
- No explanation
- No sources
- One sentence
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()