import os
import ollama

from engines.search import SearchEngine

search = SearchEngine()

MODEL = os.getenv("OLLAMA_MODEL", "gemma3")


def run(question):

    articles = search.search(question, num_results=6)

    context = "\n\n".join(
        f"TITLE: {a['title']}\n"
        f"URL: {a['url']}\n"
        f"SNIPPET: {a['snippet']}"
        for a in articles
    )

    prompt = f"""
Question:
{question}

Sources:
{context}

Create:

Position A:
(one short paragraph)

Source:
(one source URL)

Position B:
(one short paragraph)

Source:
(one source URL)

Reflection Question:
(one sentence)

Maximum 150 words.
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

    return response["message"]["content"]