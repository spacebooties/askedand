from engines.search import SearchEngine

search = SearchEngine()


def run(question):

    articles = search.search(question, num_results=3)

    output = [
        f"**Sources for:** {question}",
        ""
    ]

    for article in articles:

        output.append(
            f"**{article['title']}**\n"
            f"{article['url']}\n"
            f"Claim: {article['snippet'][:200]}...\n"
        )

    output.append(
        "\nQuestion: What evidence would most strongly challenge these claims?"
    )

    return "\n".join(output)