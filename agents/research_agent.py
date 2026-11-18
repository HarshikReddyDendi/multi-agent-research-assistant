
from tools.web_search import search_web
from llm_config import get_llm


def research_agent(topic: str):
    """
    Research Agent:
    1. Searches the web.
    2. Collects sources.
    3. Organizes findings using an LLM.
    """

    print(f"\n[Research Agent] Researching: {topic}")

    # Step 1: Search the web
    search_results = search_web(
        query=topic,
        max_results=5
    )

    if not search_results:
        raise RuntimeError("No web search results found.")

    print(f"[Research Agent] Found {len(search_results)} sources.")

    # Step 2: Prepare source information
    sources = []

    for index, result in enumerate(search_results, start=1):
        sources.append({
            "source_id": f"S{index}",
            "title": result["title"],
            "url": result["url"],
            "content": result["content"],
            "score": result["score"]
        })

    # Step 3: Prepare research context
    context = ""

    for source in sources:
        context += f"""
Source ID: {source['source_id']}
Title: {source['title']}
URL: {source['url']}
Content: {source['content']}
---
"""

    # Step 4: Ask Groq to organize findings
    llm = get_llm()

    prompt = f"""
You are a professional AI research assistant.

Research topic: {topic}

Analyze the following web search results.

Instructions:
1. Identify the most relevant information.
2. Extract important facts and key points.
3. Organize findings into clear sections.
4. Identify conflicting or uncertain information.
5. Attach source IDs such as [S1] to supported claims.
6. Never invent facts or citations.
7. If evidence is insufficient, explicitly say so.

Research sources:

{context}

Return structured research notes.
"""

    response = llm.invoke(prompt)

    print("[Research Agent] Research completed.")

    return {
        "topic": topic,
        "research_notes": response.content,
        "sources": sources
    }
