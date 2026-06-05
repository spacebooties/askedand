import os
from dotenv import load_dotenv
from exa_py import Exa

load_dotenv()


class SearchEngine:

    def __init__(self):
        self.exa = Exa(api_key=os.getenv("EXA_API_KEY"))

    def search(self, query, num_results=5):

        results = self.exa.search_and_contents(
            query,
            num_results=num_results,
            text=True
        )

        articles = []

        for result in results.results:

            text = getattr(result, "text", "") or ""

            snippet = text[:300].replace("\n", " ")

            articles.append({
                "title": result.title,
                "url": result.url,
                "snippet": snippet
            })

        return articles