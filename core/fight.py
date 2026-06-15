import os
import json
import ollama
import time

from pathlib import Path

from engines.search import SearchEngine

MODEL = os.getenv("OLLAMA_MODEL", "gemma3")

search = SearchEngine()

def run(headline):

    articles = search.search(headline, num_results=4)

    context = "\n\n".join(
        f"TITLE: {a['title']}\n"
        f"URL: {a['url']}\n"
        f"SNIPPET: {a['snippet']}"
        for a in articles
    )

    prompt = f"""
You are writing a humorous stick figure debate.

Topic:
{headline}

Sources:
{context}

Create a JSON object with EXACTLY this schema:

{{
  "title": "short title",
  "fighters": [
    {{
      "name": "Blue",
      "stance": "brief summary"
    }},
    {{
      "name": "Red",
      "stance": "brief summary"
    }}
  ],
  "dialogue": [
    {{
      "speaker": "Blue",
      "line": "short statement"
    }},
    {{
      "speaker": "Red",
      "line": "short response"
    }},
    {{
      "speaker": "Blue",
      "line": "short rebuttal"
    }},
    {{
      "speaker": "Red",
      "line": "short rebuttal"
    }}
  ],
  "final_question": "one thoughtful question"
}}

Rules:
- Return valid JSON only
- No markdown
- No code blocks
- Keep lines under 15 words
- Make each side disagree respectfully
- Use facts reflected in the sources
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    result = json.loads(content)

    Path("data").mkdir(exist_ok=True)

    filename = f"data/fight_{int(time.time())}.json"

    with open(filename, "w") as f:
        json.dump(result, f, indent=2)

    result["file"] = filename

    return result