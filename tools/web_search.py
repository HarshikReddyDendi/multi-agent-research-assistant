
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def search_web(query: str, max_results: int = 5):
    """
    Search the web using Tavily.

    Args:
        query: Research topic or search question.
        max_results: Maximum number of results.

    Returns:
        List of structured search results.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing. Check your .env file.")

    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        topic="general",
        max_results=max_results,
        include_answer=False,
        include_raw_content=False
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0.0)
        })

    return results
